import os

import cv2
import numpy as np

from config import Config


class ImageProcessor:
    """
    Image Processing Service

    Performs preprocessing before OCR and
    object detection.
    """

    def __init__(self):

        self.result_folder = Config.RESULT_FOLDER

    def process_image(self, image_path: str) -> str:
        """
        Complete preprocessing pipeline.
        """

        image = self.load_image(image_path)

        image = self.resize_image(image)

        image = self.denoise_image(image)

        image = self.improve_contrast(image)

        image = self.sharpen_image(image)

        return self.save_image(
            image,
            image_path
        )

    def load_image(self, image_path: str):
        """
        Load image using OpenCV.
        """

        if not os.path.exists(image_path):

            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        image = cv2.imread(image_path)

        if image is None:

            raise ValueError(
                "Unable to load image."
            )

        return image

    def resize_image(
        self,
        image,
        max_width: int = 1200
    ):
        """
        Resize image while preserving aspect ratio.
        """

        height, width = image.shape[:2]

        if width <= max_width:

            return image

        ratio = max_width / width

        new_size = (
            int(width * ratio),
            int(height * ratio)
        )

        return cv2.resize(
            image,
            new_size,
            interpolation=cv2.INTER_AREA
        )

    def denoise_image(self, image):
        """
        Remove image noise.
        """

        return cv2.fastNlMeansDenoisingColored(
            image,
            None,
            10,
            10,
            7,
            21
        )

    def improve_contrast(self, image):
        """
        Improve image contrast using CLAHE.
        """

        lab = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2LAB
        )

        l, a, b = cv2.split(lab)

        clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8, 8)
        )

        l = clahe.apply(l)

        merged = cv2.merge(
            (l, a, b)
        )

        return cv2.cvtColor(
            merged,
            cv2.COLOR_LAB2BGR
        )

    def sharpen_image(self, image):
        """
        Sharpen image.
        """

        kernel = np.array(
            [
                [0, -1, 0],
                [-1, 5, -1],
                [0, -1, 0]
            ]
        )

        return cv2.filter2D(
            image,
            -1,
            kernel
        )

    def convert_to_grayscale(self, image):
        """
        Convert image to grayscale.
        """

        return cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

    def threshold_image(self, image):
        """
        Apply Otsu thresholding.
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

    def save_image(
        self,
        image,
        original_path: str
    ) -> str:
        """
        Save processed image.
        """

        filename = os.path.basename(
            original_path
        )

        output_path = os.path.join(
            self.result_folder,
            filename
        )

        success = cv2.imwrite(
            output_path,
            image
        )

        if not success:

            raise IOError(
                "Failed to save processed image."
            )

        return output_path