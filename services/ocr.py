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


logger = logging.getLogger(__name__)


# ============================================================
# Type Alias
# ============================================================

OCRResult = Tuple[Any, str, float]


class OCRService:
    """
    Optical Character Recognition Service.

    Uses EasyOCR to detect and extract text from images.
    """

    def __init__(self):

        self.languages = Config.OCR_LANGUAGES

        self.min_confidence = (
            Config.OCR_MIN_CONFIDENCE
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
    # EXTRACT TEXT
    # ========================================================

    def extract_text(
        self,
        image_path: str
    ) -> str:

        try:

            results = self._read_image(
                image_path
            )

            return self.process_results(
                results
            )

        except Exception:
            logger.exception(
                "OCR processing failed: %s",
                image_path
            )

            return "OCR processing failed."

    # ========================================================
    # EXTRACT DETAILS
    # ========================================================

    def extract_details(
        self,
        image_path: str
    ) -> List[Dict[str, Any]]:

        try:

            results = self._read_image(
                image_path
            )

            return self._process_detailed_results(
                results
            )

        except Exception:
            logger.exception(
                "Detailed OCR failed: %s",
                image_path
            )

            return []

    # ========================================================
    # READ IMAGE
    # ========================================================

    def _read_image(
        self,
        image_path: str
    ) -> List[OCRResult]:

        image = self.load_image(
            image_path
        )

        prepared_image = self.prepare_image(
            image
        )

        results = self.reader.readtext(
            prepared_image,
            detail=1,
            paragraph=False
        )

        if not isinstance(
            results,
            list
        ):
            logger.warning(
                "Unexpected EasyOCR result type: %s",
                type(results).__name__
            )

            return []

        return results

    # ========================================================
    # LOAD IMAGE
    # ========================================================

    def load_image(
        self,
        image_path: str
    ):

        if not image_path:
            raise ValueError(
                "Image path cannot be empty."
            )

        if not os.path.isfile(
            image_path
        ):
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        image = cv2.imread(
            image_path
        )

        if image is None:
            raise ValueError(
                f"Unable to read image: {image_path}"
            )

        return image

    # ========================================================
    # PREPARE IMAGE
    # ========================================================

    def prepare_image(
        self,
        image
    ):

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
    # PROCESS RESULTS
    # ========================================================

    def process_results(
        self,
        results: Any
    ) -> str:

        if not results:
            return "No readable text found."

        extracted_text = []

        for result in results:

            parsed_result = self._parse_result(
                result
            )

            if parsed_result is None:
                continue

            _, text, confidence = (
                parsed_result
            )

            if confidence < self.min_confidence:
                continue

            extracted_text.append(
                text
            )

        if not extracted_text:
            return "No readable text found."

        return "\n".join(
            extracted_text
        )

    # ========================================================
    # DETAILED RESULTS
    # ========================================================

    def _process_detailed_results(
        self,
        results: Any
    ) -> List[Dict[str, Any]]:

        if not results:
            return []

        details = []

        for result in results:

            parsed_result = self._parse_result(
                result
            )

            if parsed_result is None:
                continue

            bbox, text, confidence = (
                parsed_result
            )

            if confidence < self.min_confidence:
                continue

            details.append(
                {
                    "text": text,
                    "confidence": round(
                        confidence * 100,
                        2
                    ),
                    "bounding_box": bbox
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
                "Skipping OCR result with length: %d",
                len(result)
            )

            return None

        bbox, text, confidence = result

        # ----------------------------------------------------
        # Validate text
        # ----------------------------------------------------

        if not isinstance(
            text,
            str
        ):
            return None

        text = text.strip()

        if not text:
            return None

        # ----------------------------------------------------
        # Validate confidence
        # ----------------------------------------------------

        try:
            confidence = float(
                confidence
            )

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

        # ----------------------------------------------------
        # Validate bounding box
        # ----------------------------------------------------

        if bbox is None:
            return None

        if not isinstance(
            bbox,
            (list, tuple)
        ):
            return None

        return (
            bbox,
            text,
            confidence
        )