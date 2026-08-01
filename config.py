import os


class Config:
    """
    Application Configuration
    """

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "my-secret-key"
    )

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

    RESULT_FOLDER = os.path.join(BASE_DIR, "results")

    MODEL_PATH = os.path.join(
        BASE_DIR,
        "models",
        "yolov8n.pt"
    )

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg",
        "bmp",
        "webp"
    }

    OCR_LANGUAGES = ["en"]

    DETECTION_CONFIDENCE = 0.40

    IMAGE_SIZE = 640

    @staticmethod
    def create_directories():
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.RESULT_FOLDER, exist_ok=True)
        os.makedirs(os.path.dirname(Config.MODEL_PATH), exist_ok=True)