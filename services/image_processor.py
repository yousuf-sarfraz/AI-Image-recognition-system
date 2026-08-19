import os
from typing import Optional

import cv2
import numpy as np

from config import Config


class ImageProcessor:
    """
    Image Processing Service

    Provides image loading, resizing, denoising,
    contrast enhancement, sharpening, grayscale
    conversion, thresholding, and saving.
    """

    def __init__(self):
        self.result_folder = Config.RESULT_FOLDER
        self.max_width = Config.IMAGE_SIZE

        # Make sure the result folder exists
        os.makedirs(self.result_folder, exist_ok=True)

    # ==========================================================
    # MAIN PROCESSING
    # ==========================================================

    def process_image(
        self,
        image_path: str,
        save_result: bool = True
    ) -> str:
        """
        Run the complete image preprocessing pipeline.

        Parameters
        ----------
        image_path : str
            Path of the original image.

        save_result : bool
            Whether to save the processed image.

        Returns
        -------
        str
            Path of the processed image.
        """

        image = self.load_image(image_path)

        image = self.resize_image(image)
        image = self.denoise_image(image)
        image = self.improve_contrast(image)
        image = self.sharpen_image(image)

        if save_result:
            return self.save_image(
                image,
                image_path
            )

        return image_path

    def process_for_ocr(
        self,
        image_path: str
    ) -> str:
        """
        Prepare an image specifically for OCR.

        OCR generally works better with a clean,
        high-contrast grayscale image.
        """

        image = self.load_image(image_path)

        image = self.resize_image(image)
        image = self.denoise_image(image)
        image = self.improve_contrast(image)
        image = self.sharpen_image(image)

        gray = self.convert_to_grayscale(image)

        threshold = self.threshold_image(gray)

        return self.save_processed_image(
            threshold,
            image_path,
            suffix="_ocr"
        )

    # ==========================================================
    # IMAGE LOADING
    # ==========================================================

    def load_image(self, image_path: str):
        """
        Load an image using OpenCV.

        Raises
        ------
        FileNotFoundError
            If the image does not exist.

        ValueError
            If OpenCV cannot read the image.
        """

        if not image_path:
            raise ValueError("Image path cannot be empty.")

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

    # ==========================================================
    # RESIZING
    # ==========================================================

    def resize_image(
        self,
        image,
        max_width: Optional[int] = None
    ):
        """
        Resize image while preserving aspect ratio.

        Images smaller than max_width are not enlarged.
        """

        if image is None:
            raise ValueError(
                "Cannot resize an empty image."
            )

        if max_width is None:
            max_width = self.max_width

        height, width = image.shape[:2]

        if width <= max_width:
            return image

        ratio = max_width / width

        new_width = int(width * ratio)
        new_height = int(height * ratio)

        return cv2.resize(
            image,
            (new_width, new_height),
            interpolation=cv2.INTER_AREA
        )

    # ==========================================================
    # DENOISING
    # ==========================================================

    def denoise_image(self, image):
        """
        Remove noise from a color image.
        """

        if image is None:
            raise ValueError(
                "Cannot denoise an empty image."
            )

        return cv2.fastNlMeansDenoisingColored(
            image,
            None,
            10,
            10,
            7,
            21
        )

    # ==========================================================
    # CONTRAST
    # ==========================================================

    def improve_contrast(self, image):
        """
        Improve image contrast using CLAHE.

        CLAHE enhances local contrast while helping
        preserve image details.
        """

        if image is None:
            raise ValueError(
                "Cannot improve contrast of an empty image."
            )

        lab = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2LAB
        )

        l_channel, a_channel, b_channel = cv2.split(lab)

        clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8, 8)
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

    # ==========================================================
    # SHARPENING
    # ==========================================================

    def sharpen_image(self, image):
        """
        Sharpen image details.
        """

        if image is None:
            raise ValueError(
                "Cannot sharpen an empty image."
            )

        kernel = np.array(
            [
                [0, -1, 0],
                [-1, 5, -1],
                [0, -1, 0]
            ],
            dtype=np.float32
        )

        return cv2.filter2D(
            image,
            -1,
            kernel
        )

    # ==========================================================
    # GRAYSCALE
    # ==========================================================

    def convert_to_grayscale(self, image):
        """
        Convert BGR image to grayscale.
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

    # ==========================================================
    # THRESHOLDING
    # ==========================================================

    def threshold_image(self, image):
        """
        Apply Otsu binary thresholding.

        Converts the image into a black-and-white
        representation useful for OCR.
        """

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

    # ==========================================================
    # SAVE IMAGE
    # ==========================================================

    def save_image(
        self,
        image,
        original_path: str
    ) -> str:
        """
        Save a processed image using the original filename.
        """

        return self.save_processed_image(
            image,
            original_path,
            suffix="_processed"
        )

    def save_processed_image(
        self,
        image,
        original_path: str,
        suffix: str = "_processed"
    ) -> str:
        """
        Save a processed image with a unique suffix.

        Example:
            image.jpg
            image_processed.jpg
            image_ocr.jpg
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

        output_filename = (
            f"{name}{suffix}{extension}"
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

        return output_path