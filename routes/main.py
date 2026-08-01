from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    current_app,
)

from werkzeug.utils import secure_filename

import os
import uuid

from services.ocr import OCRService
from services.detector import ObjectDetector
from services.image_processor import ImageProcessor

main = Blueprint("main", __name__)

ocr_service = OCRService()
object_detector = ObjectDetector()
image_processor = ImageProcessor()


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


@main.route("/")
def home():
    return render_template("index.html")


@main.route("/about")
def about():
    return render_template("about.html")


@main.route("/upload", methods=["POST"])
def upload():

    if "image" not in request.files:
        return redirect(url_for("main.home"))

    image = request.files["image"]

    if image.filename == "":
        return redirect(url_for("main.home"))

    if not allowed_file(image.filename):
        return redirect(url_for("main.home"))

    filename = f"{uuid.uuid4()}_{secure_filename(image.filename)}"

    upload_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        filename,
    )

    image.save(upload_path)

    try:
        processed_image = image_processor.process_image(upload_path)

        extracted_text = ocr_service.extract_text(processed_image)

        detected_objects = object_detector.detect_objects(processed_image)

    except Exception as e:
        return f"Error: {e}", 500

    return render_template(
        "result.html",
        image=filename,
        text=extracted_text,
        objects=detected_objects,
    )