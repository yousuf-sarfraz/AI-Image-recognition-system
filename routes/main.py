# ============================================================
# Routes
# Image & Text Recognition AI
# ============================================================

import logging
import os

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
# AI Services
# ============================================================

ocr_service = OCRService()

object_detector = ObjectDetector()

image_processor = ImageProcessor()


# ============================================================
# Home Route
# ============================================================

@main.route("/")
def home():
    """
    Display the main ImageAI page.
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
        Save Image
          ↓
        Image Preprocessing
          ↓
        OCR
          ↓
        Object Detection
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
    # File Processing
    # ========================================================

    upload_path = None
    filename = None

    try:

        # ----------------------------------------------------
        # Save Uploaded File
        # ----------------------------------------------------

        upload_path, filename = save_uploaded_file(
            image,
            current_app.config["UPLOAD_FOLDER"]
        )

        logger.info(
            "Image uploaded successfully: %s",
            filename
        )


        # ----------------------------------------------------
        # Image Preprocessing
        # ----------------------------------------------------

        processed_image = image_processor.process_image(
            upload_path
        )

        logger.info(
            "Image preprocessing completed: %s",
            filename
        )


        # ----------------------------------------------------
        # OCR
        # ----------------------------------------------------

        extracted_text = ocr_service.extract_text(
            processed_image
        )

        logger.info(
            "OCR completed: %s",
            filename
        )


        # ----------------------------------------------------
        # Object Detection
        # ----------------------------------------------------

        detected_objects = object_detector.detect_objects(
            processed_image
        )

        logger.info(
            "Object detection completed: %s",
            filename
        )


        # ----------------------------------------------------
        # Processing Complete
        # ----------------------------------------------------

        logger.info(
            "Image processing completed successfully: %s",
            filename
        )


    except Exception as error:

        logger.exception(
            "Error while processing image '%s': %s",
            filename,
            error
        )


        # ----------------------------------------------------
        # Cleanup Uploaded File
        # ----------------------------------------------------

        if upload_path:

            delete_file(
                upload_path
            )


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