# ============================================================
# Routes
# Image & Text Recognition AI
# ============================================================

import logging

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from services.detector import ObjectDetector
from services.image_processor import ImageProcessor
from services.ocr import OCRService

from utils import (
    allowed_file,
    save_uploaded_file,
    delete_file,
)


# ============================================================
# Blueprint
# ============================================================

main = Blueprint(
    "main",
    __name__
)


# ============================================================
# Logger
# ============================================================

logger = logging.getLogger(__name__)


# ============================================================
# Service Initialization
# ============================================================

def get_ocr_service() -> OCRService:
    """
    Return the shared OCR service instance.

    The service is created only when it is first needed.
    """

    if "ocr_service" not in current_app.extensions:
        logger.info("Initializing OCR service.")

        current_app.extensions["ocr_service"] = OCRService()

    return current_app.extensions["ocr_service"]


def get_object_detector() -> ObjectDetector:
    """
    Return the shared object detector instance.

    The YOLO model is created only when it is first needed.
    """

    if "object_detector" not in current_app.extensions:
        logger.info("Initializing object detection service.")

        current_app.extensions["object_detector"] = ObjectDetector()

    return current_app.extensions["object_detector"]


def get_image_processor() -> ImageProcessor:
    """
    Return the shared image processor instance.

    The service is created only when it is first needed.
    """

    if "image_processor" not in current_app.extensions:
        logger.info("Initializing image processing service.")

        current_app.extensions["image_processor"] = ImageProcessor()

    return current_app.extensions["image_processor"]


# ============================================================
# Home Route
# ============================================================

@main.route("/")
def home():
    """
    Display the main Image & Text Recognition AI page.
    """

    return render_template(
        "index.html"
    )


# ============================================================
# About Route
# ============================================================

@main.route("/about")
def about():
    """
    Display the About page.
    """

    return render_template(
        "about.html"
    )


# ============================================================
# Upload Route
# ============================================================

@main.route(
    "/upload",
    methods=["POST"]
)
def upload():
    """
    Handle image upload and AI processing.

    Processing pipeline:

        Upload
          ↓
        Validate
          ↓
        Save Original Image
          ↓
        OCR Preprocessing
          ↓
        OCR
          ↓
        YOLO Object Detection
          ↓
        Results Page
    """

    # ========================================================
    # Check File
    # ========================================================

    if "image" not in request.files:

        flash(
            "Please select an image to upload.",
            "error"
        )

        return redirect(
            url_for("main.home")
        )

    image = request.files["image"]


    # ========================================================
    # Check Filename
    # ========================================================

    if not image.filename:

        flash(
            "Please select an image to upload.",
            "error"
        )

        return redirect(
            url_for("main.home")
        )


    # ========================================================
    # Validate File Type
    # ========================================================

    if not allowed_file(image.filename):

        flash(
            "Invalid file type. "
            "Please upload PNG, JPG, JPEG, BMP, or WEBP.",
            "error"
        )

        return redirect(
            url_for("main.home")
        )


    # ========================================================
    # File Variables
    # ========================================================

    upload_path = None
    filename = None
    ocr_image_path = None


    try:

        # ====================================================
        # Save Original Uploaded Image
        # ====================================================

        upload_path, filename = save_uploaded_file(
            image,
            current_app.config["UPLOAD_FOLDER"]
        )

        logger.info(
            "Image uploaded successfully: %s",
            filename
        )


        # ====================================================
        # Get Services
        # ====================================================

        image_processor = get_image_processor()
        ocr_service = get_ocr_service()
        object_detector = get_object_detector()


        # ====================================================
        # OCR PREPROCESSING
        # ====================================================
        #
        # OCR gets a specially prepared image.
        #
        # This uses:
        # resize
        # denoise
        # contrast enhancement
        # sharpening
        # grayscale
        # thresholding
        #
        # ====================================================

        ocr_image_path = image_processor.process_for_ocr(
            upload_path
        )

        logger.info(
            "OCR preprocessing completed: %s",
            filename
        )


        # ====================================================
        # OCR
        # ====================================================

        extracted_text = ocr_service.extract_text(
            ocr_image_path
        )

        logger.info(
            "OCR completed: %s",
            filename
        )


        # ====================================================
        # OBJECT DETECTION
        # ====================================================
        #
        # YOLO receives the ORIGINAL image instead of the
        # heavily processed OCR image.
        #
        # This preserves the original visual information.
        #
        # ====================================================

        detected_objects = object_detector.detect_objects(
            upload_path
        )

        logger.info(
            "Object detection completed: %s",
            filename
        )


        # ====================================================
        # Processing Complete
        # ====================================================

        logger.info(
            "Image processing completed successfully: %s",
            filename
        )


    except FileNotFoundError as error:

        logger.exception(
            "Required file or model was not found: %s",
            error
        )

        if upload_path:
            delete_file(upload_path)

        if ocr_image_path:
            delete_file(ocr_image_path)

        flash(
            "A required file or AI model could not be found.",
            "error"
        )

        return redirect(
            url_for("main.home")
        )


    except ValueError as error:

        logger.exception(
            "Invalid image or input data: %s",
            error
        )

        if upload_path:
            delete_file(upload_path)

        if ocr_image_path:
            delete_file(ocr_image_path)

        flash(
            "The uploaded image could not be processed. "
            "Please try another image.",
            "error"
        )

        return redirect(
            url_for("main.home")
        )


    except Exception as error:

        logger.exception(
            "Error while processing image '%s': %s",
            filename,
            error
        )

        # ----------------------------------------------------
        # Cleanup Uploaded Image
        # ----------------------------------------------------

        if upload_path:
            delete_file(upload_path)

        # ----------------------------------------------------
        # Cleanup OCR Image
        # ----------------------------------------------------

        if ocr_image_path:
            delete_file(ocr_image_path)

        flash(
            "Something went wrong while processing "
            "the image. Please try again.",
            "error"
        )

        return redirect(
            url_for("main.home")
        )


    # ========================================================
    # Display Results
    # ========================================================

    return render_template(
        "result.html",
        image=filename,
        text=extracted_text,
        objects=detected_objects,
    )