# ============================================================
# Image Processing Service
# Image & Text Recognition AI
# ============================================================

import logging
import os
import uuid
from typing import Optional

import cv2
import numpy as np

from config import Config


# ============================================================
# Logger
# ============================================================

logger = logging.getLogger(__name__)


# ============================================================
# Image Processing Service
# ============================================================

class ImageProcessor:
    """
    Image Processing Service.

    Provides separate processing pipelines for:

    1. General image processing
    2. OCR-specific image preparation

    Supported operations include:

    - Image loading
    - Resizing
    - Denoising
    - Contrast enhancement
    - Sharpening
    - Grayscale conversion
    - Thresholding
    - Processed image saving
    """

    def __init__(self):
        """
        Initialize the image processor using
        centralized application configuration.
        """

        self.result_folder = Config.RESULT_FOLDER
        self.max_width = Config.IMAGE_SIZE

        # Make sure the result directory exists.
        os.makedirs(
            self.result_folder,
            exist_ok=True
        )

        logger.info(
            "ImageProcessor initialized. Result folder: %s",
            self.result_folder
        )

    # ========================================================
    # MAIN PROCESSING
    # ========================================================

    def process_image(
        self,
        image_path: str,
        save_result: bool = True
    ) -> str:
        """
        Run the general image-processing pipeline.

        Pipeline:

            Load
              ↓
            Resize
              ↓
            Denoise
              ↓
            Improve Contrast
              ↓
            Sharpen
              ↓
            Save

        Parameters
        ----------
        image_path : str
            Path to the original image.

        save_result : bool
            Whether to save the processed image.

        Returns
        -------
        str
            Path to the processed image when saved.

        Notes
        -----
        When save_result is False, the original path is
        returned for backward compatibility.
        """

        image = self.load_image(
            image_path
        )

        image = self.resize_image(
            image
        )

        image = self.denoise_image(
            image
        )

        image = self.improve_contrast(
            image
        )

        image = self.sharpen_image(
            image
        )

        if not save_result:
            return image_path

        return self.save_image(
            image,
            image_path
        )

    # ========================================================
    # OCR PROCESSING
    # ========================================================

    def process_for_ocr(
        self,
        image_path: str
    ) -> str:
        """
        Prepare an image specifically for OCR.

        Pipeline:

            Load
              ↓
            Resize
              ↓
            Denoise
              ↓
            Improve Contrast
              ↓
            Sharpen
              ↓
            Grayscale
              ↓
            Otsu Threshold
              ↓
            Save

        Parameters
        ----------
        image_path : str
            Path to the original image.

        Returns
        -------
        str
            Path to the OCR-processed image.
        """

        image = self.load_image(
            image_path
        )

        image = self.resize_image(
            image
        )

        image = self.denoise_image(
            image
        )

        image = self.improve_contrast(
            image
        )

        image = self.sharpen_image(
            image
        )

        gray = self.convert_to_grayscale(
            image
        )

        threshold = self.threshold_image(
            gray
        )

        return self.save_processed_image(
            threshold,
            image_path,
            suffix="_ocr"
        )

    # ========================================================
    # LOAD IMAGE
    # ========================================================

    def load_image(
        self,
        image_path: str
    ):
        """
        Load an image using OpenCV.

        Raises
        ------
        ValueError
            If the image path is empty or OpenCV
            cannot read the image.

        FileNotFoundError
            If the image does not exist.
        """

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
    # RESIZE
    # ========================================================

    def resize_image(
        self,
        image,
        max_width: Optional[int] = None
    ):
        """
        Resize an image while preserving aspect ratio.

        Images smaller than max_width are not enlarged.

        Parameters
        ----------
        image
            OpenCV image.

        max_width : int | None
            Maximum allowed image width.
            Uses Config.IMAGE_SIZE when omitted.
        """

        if image is None:
            raise ValueError(
                "Cannot resize an empty image."
            )

        if max_width is None:
            max_width = self.max_width

        if max_width <= 0:
            raise ValueError(
                "max_width must be greater than zero."
            )

        height, width = image.shape[:2]

        if width <= max_width:
            return image

        ratio = max_width / width

        new_width = max(
            1,
            int(width * ratio)
        )

        new_height = max(
            1,
            int(height * ratio)
        )

        return cv2.resize(
            image,
            (
                new_width,
                new_height
            ),
            interpolation=cv2.INTER_AREA
        )

    # ========================================================
    # DENOISING
    # ========================================================

    def denoise_image(
        self,
        image
    ):
        """
        Remove noise from a color image.

        The denoising parameters come from Config.
        """

        if image is None:
            raise ValueError(
                "Cannot denoise an empty image."
            )

        # fastNlMeansDenoisingColored requires
        # a 3-channel color image.
        if len(image.shape) != 3:
            return image

        return cv2.fastNlMeansDenoisingColored(
            image,
            None,
            Config.DENOISE_H,
            Config.DENOISE_H_COLOR,
            Config.DENOISE_TEMPLATE_WINDOW,
            Config.DENOISE_SEARCH_WINDOW
        )

    # ========================================================
    # CONTRAST
    # ========================================================

    def improve_contrast(
        self,
        image
    ):
        """
        Improve local image contrast using CLAHE.

        CLAHE is applied to the luminance channel
        when processing a color image.

        Configuration values are loaded from Config.
        """

        if image is None:
            raise ValueError(
                "Cannot improve contrast of an empty image."
            )

        clahe = cv2.createCLAHE(
            clipLimit=Config.CLAHE_CLIP_LIMIT,
            tileGridSize=Config.CLAHE_TILE_GRID_SIZE
        )

        # Grayscale image
        if len(image.shape) == 2:

            return clahe.apply(
                image
            )

        # Color image
        lab = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2LAB
        )

        l_channel, a_channel, b_channel = (
            cv2.split(lab)
        )

        l_channel = clahe.apply(
            l_channel
        )

        merged = cv2.merge(
            (
                l_channel,
                a_channel,
                b_channel
            )
        )

        return cv2.cvtColor(
            merged,
            cv2.COLOR_LAB2BGR
        )

    # ========================================================
    # SHARPEN
    # ========================================================

    def sharpen_image(
        self,
        image
    ):
        """
        Sharpen image details using the configured
        sharpening kernel.
        """

        if image is None:
            raise ValueError(
                "Cannot sharpen an empty image."
            )

        kernel = np.array(
            Config.SHARPEN_KERNEL,
            dtype=np.float32
        )

        return cv2.filter2D(
            image,
            -1,
            kernel
        )

    # ========================================================
    # GRAYSCALE
    # ========================================================

    def convert_to_grayscale(
        self,
        image
    ):
        """
        Convert a BGR image to grayscale.

        If the image is already grayscale,
        it is returned unchanged.
        """

        if image is None:
            raise ValueError(
                "Cannot convert an empty image."
            )

        if len(image.shape) == 2:
            return image

        return cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

    # ========================================================
    # THRESHOLD
    # ========================================================

    def threshold_image(
        self,
        image
    ):
        """
        Apply Otsu binary thresholding.

        Otsu automatically determines a suitable
        threshold value for the grayscale image.
        """

        if image is None:
            raise ValueError(
                "Cannot threshold an empty image."
            )

        gray = self.convert_to_grayscale(
            image
        )

        _, threshold = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        return threshold

    # ========================================================
    # SAVE IMAGE
    # ========================================================

    def save_image(
        self,
        image,
        original_path: str
    ) -> str:
        """
        Save a generally processed image.

        A unique filename is generated to prevent
        conflicts between multiple uploads.
        """

        return self.save_processed_image(
            image,
            original_path,
            suffix="_processed"
        )

    # ========================================================
    # SAVE PROCESSED IMAGE
    # ========================================================

    def save_processed_image(
        self,
        image,
        original_path: str,
        suffix: str = "_processed"
    ) -> str:
        """
        Save a processed image using a unique filename.

        Examples
        --------
        original.jpg

        original_processed_a1b2c3d4.jpg

        original_ocr_e5f6g7h8.jpg
        """

        if image is None:
            raise ValueError(
                "Cannot save an empty image."
            )

        if not original_path:
            raise ValueError(
                "Original image path cannot be empty."
            )

        filename = os.path.basename(
            original_path
        )

        name, extension = os.path.splitext(
            filename
        )

        if not extension:
            raise ValueError(
                "Original image must have an extension."
            )

        unique_id = uuid.uuid4().hex[:8]

        output_filename = (
            f"{name}"
            f"{suffix}"
            f"_{unique_id}"
            f"{extension}"
        )

        output_path = os.path.join(
            self.result_folder,
            output_filename
        )

        success = cv2.imwrite(
            output_path,
            image
        )

        if not success:
            raise IOError(
                f"Failed to save processed image: "
                f"{output_path}"
            )

        logger.info(
            "Processed image saved successfully: %s",
            output_path
        )

        return output_path