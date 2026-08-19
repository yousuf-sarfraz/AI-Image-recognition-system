import os


class Config:
    """
    Application Configuration

    Contains all configuration settings used by the
    AI Image Recognition System.
    """

    # Project Base Directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Flask Secret Key
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "dev-secret-key"
    )

    # Upload and Result Directories
    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "uploads"
    )

    RESULT_FOLDER = os.path.join(
        BASE_DIR,
        "results"
    )

    # YOLO Model Path
    MODEL_PATH = os.path.join(
        BASE_DIR,
        "models",
        "yolov8n.pt"
    )

    # Maximum Upload Size: 16 MB
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # Allowed Image Extensions
    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg",
        "bmp",
        "webp"
    }

    # OCR Configuration
    OCR_LANGUAGES = ["en"]

    # YOLO Detection Configuration
    DETECTION_CONFIDENCE = 0.40
    IMAGE_SIZE = 640

    @staticmethod
    def create_directories():
        """
        Create required application directories
        if they do not already exist.
        """

        os.makedirs(
            Config.UPLOAD_FOLDER,
            exist_ok=True
        )

        os.makedirs(
            Config.RESULT_FOLDER,
            exist_ok=True
        )

        os.makedirs(
            os.path.dirname(Config.MODEL_PATH),
            exist_ok=True
        )