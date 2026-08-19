# ============================================================
# OCR Service
# Image & Text Recognition AI
# ============================================================

import logging
import os
from typing import Any, Dict, List, Optional, Tuple

import cv2
import easyocr

from config import Config


# ============================================================
# Logger
# ============================================================

logger = logging.getLogger(__name__)


# ============================================================
# Type Aliases
# ============================================================

OCRResult = Tuple[Any, str, float]


# ============================================================
# OCR Service
# ============================================================

class OCRService:
    """
    Optical Character Recognition Service.

    Uses EasyOCR to detect and extract text from images.
    """

    def __init__(self):
        """
        Initialize the EasyOCR reader and configuration.
        """

        self.languages = Config.OCR_LANGUAGES

        self.min_confidence = getattr(
            Config,
            "OCR_MIN_CONFIDENCE",
            0.30
        )

        logger.info(
            "Initializing EasyOCR with languages: %s",
            self.languages
        )

        try:
            self.reader = easyocr.Reader(
                self.languages,
                gpu=False
            )

        except Exception:
            logger.exception(
                "Failed to initialize EasyOCR."
            )
            raise

        logger.info(
            "EasyOCR initialized successfully."
        )

    # ========================================================
    # PUBLIC API
    # ========================================================

    def extract_text(
        self,
        image_path: str
    ) -> str:
        """
        Extract readable text from an image.

        Returns
        -------
        str
            Extracted text or an informative message.
        """

        try:
            results = self._read_image(image_path)

            return self.process_results(results)

        except Exception:
            logger.exception(
                "OCR processing failed for: %s",
                image_path
            )

            return "OCR processing failed."

    def extract_details(
        self,
        image_path: str
    ) -> List[Dict[str, Any]]:
        """
        Extract detailed OCR information.

        Each detected item contains:

        - text
        - confidence
        - bounding_box
        """

        try:
            results = self._read_image(image_path)

            return self._process_detailed_results(
                results
            )

        except Exception:
            logger.exception(
                "Detailed OCR failed for: %s",
                image_path
            )

            return []

    # ========================================================
    # EASY OCR
    # ========================================================

    def _read_image(
        self,
        image_path: str
    ) -> List[OCRResult]:
        """
        Load an image, prepare it, and run EasyOCR.
        """

        image = self.load_image(image_path)

        prepared_image = self.prepare_image(image)

        results = self.reader.readtext(
            prepared_image,
            detail=1,
            paragraph=False
        )

        return results

    # ========================================================
    # IMAGE LOADING
    # ========================================================

    def load_image(
        self,
        image_path: str
    ):
        """
        Load an image using OpenCV.
        """

        if not image_path:
            raise ValueError(
                "Image path cannot be empty."
            )

        if not os.path.isfile(image_path):
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        image = cv2.imread(image_path)

        if image is None:
            raise ValueError(
                f"Unable to read image: {image_path}"
            )

        return image

    # ========================================================
    # IMAGE PREPARATION
    # ========================================================

    def prepare_image(
        self,
        image
    ):
        """
        Prepare an OpenCV image for EasyOCR.

        Converts BGR images to RGB.
        """

        if image is None:
            raise ValueError(
                "Cannot prepare an empty image."
            )

        if len(image.shape) == 2:
            return image

        return cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

    # ========================================================
    # RESULT PROCESSING
    # ========================================================

    def process_results(
        self,
        results: Any
    ) -> str:
        """
        Convert EasyOCR results into readable text.
        """

        if not results:
            return "No readable text found."

        extracted_text: List[str] = []

        for result in results:

            parsed_result = self._parse_result(
                result
            )

            if parsed_result is None:
                continue

            _, text, confidence = parsed_result

            if confidence < self.min_confidence:
                continue

            extracted_text.append(text)

        if not extracted_text:
            return "No readable text found."

        return "\n".join(extracted_text)

    # ========================================================
    # DETAILED RESULT PROCESSING
    # ========================================================

    def _process_detailed_results(
        self,
        results: Any
    ) -> List[Dict[str, Any]]:
        """
        Convert EasyOCR results into detailed dictionaries.
        """

        if not results:
            return []

        details: List[Dict[str, Any]] = []

        for result in results:

            parsed_result = self._parse_result(
                result
            )

            if parsed_result is None:
                continue

            bbox, text, confidence = parsed_result

            if confidence < self.min_confidence:
                continue

            details.append(
                {
                    "text": text,
                    "confidence": round(
                        confidence * 100,
                        2
                    ),
                    "bounding_box": bbox,
                }
            )

        return details

    # ========================================================
    # RESULT VALIDATION
    # ========================================================

    def _parse_result(
        self,
        result: Any
    ) -> Optional[OCRResult]:
        """
        Safely validate and parse one EasyOCR result.

        Returns
        -------
        tuple or None
            (bounding_box, text, confidence)
        """

        if not isinstance(
            result,
            (list, tuple)
        ):
            logger.warning(
                "Skipping invalid OCR result type: %s",
                type(result).__name__
            )
            return None

        if len(result) != 3:
            logger.warning(
                "Skipping OCR result with unexpected length: %s",
                len(result)
            )
            return None

        bbox, text, confidence = result

        if not isinstance(text, str):
            return None

        text = text.strip()

        if not text:
            return None

        try:
            confidence = float(confidence)

        except (
            TypeError,
            ValueError
        ):
            return None

        if not 0.0 <= confidence <= 1.0:
            logger.warning(
                "Invalid OCR confidence: %s",
                confidence
            )
            return None

        return (
            bbox,
            text,
            confidence
        )