# ============================================================
# Application Configuration
# Image & Text Recognition AI
# ============================================================

import os


class Config:
    """
    Central configuration for the Image & Text Recognition AI
    application.

    All major application settings are kept here so that
    services can use a single configuration source.
    """

    # ========================================================
    # PROJECT DIRECTORIES
    # ========================================================

    BASE_DIR = os.path.abspath(
        os.path.dirname(__file__)
    )

    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "uploads"
    )

    RESULT_FOLDER = os.path.join(
        BASE_DIR,
        "results"
    )

    MODEL_PATH = os.path.join(
        BASE_DIR,
        "models",
        "yolov8n.pt"
    )

    # ========================================================
    # FLASK CONFIGURATION
    # ========================================================

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "dev-secret-key"
    )

    # Maximum upload size: 16 MB
    MAX_CONTENT_LENGTH = (
        16 * 1024 * 1024
    )

    # ========================================================
    # FILE CONFIGURATION
    # ========================================================

    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg",
        "bmp",
        "webp"
    }

    # ========================================================
    # IMAGE PROCESSING CONFIGURATION
    # ========================================================

    # Maximum width used when resizing images.
    IMAGE_SIZE = 640

    # --------------------------------------------------------
    # Denoising
    # --------------------------------------------------------

    DENOISE_H = 10
    DENOISE_H_COLOR = 10
    DENOISE_TEMPLATE_WINDOW = 7
    DENOISE_SEARCH_WINDOW = 21

    # --------------------------------------------------------
    # Contrast Enhancement
    # --------------------------------------------------------

    CLAHE_CLIP_LIMIT = 2.0

    CLAHE_TILE_GRID_SIZE = (
        8,
        8
    )

    # --------------------------------------------------------
    # Sharpening
    # --------------------------------------------------------

    SHARPEN_KERNEL = (
        (0, -1, 0),
        (-1, 5, -1),
        (0, -1, 0)
    )

    # --------------------------------------------------------
    # OCR Thresholding
    # --------------------------------------------------------

    OCR_THRESHOLD_TYPE = (
        "binary_otsu"
    )

    # ========================================================
    # OCR CONFIGURATION
    # ========================================================

    OCR_LANGUAGES = [
        "en"
    ]

    OCR_MIN_CONFIDENCE = 0.30

    # ========================================================
    # YOLO CONFIGURATION
    # ========================================================

    DETECTION_CONFIDENCE = 0.40

    # ========================================================
    # DIRECTORY CREATION
    # ========================================================

    @classmethod
    def create_directories(cls):
        """
        Create all required application directories.
        """

        directories = [
            cls.UPLOAD_FOLDER,
            cls.RESULT_FOLDER,
            os.path.dirname(
                cls.MODEL_PATH
            )
        ]

        for directory in directories:

            os.makedirs(
                directory,
                exist_ok=True
            )