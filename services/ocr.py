import os
import traceback
import cv2
import easyocr

from config import Config


class OCRService:

    def __init__(self):
        self.reader = easyocr.Reader(
            Config.OCR_LANGUAGES,
            gpu=False
        )
        self.min_confidence = 0.30

    def extract_text(self, image_path: str):

        if not os.path.exists(image_path):
            return "Image not found."

        try:

            image = cv2.imread(image_path)

            if image is None:
                return "Could not read image."

            # Convert to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            results = self.reader.readtext(
                image,
                detail=1,
                paragraph=False
            )

            extracted_text = []

            for result in results:

                if len(result) != 3:
                    continue

                bbox, text, confidence = result

                if confidence >= self.min_confidence:
                    extracted_text.append(text.strip())

            if extracted_text:
                return "\n".join(extracted_text)

            return "No readable text found."

        except Exception:
            print("========== OCR ERROR ==========")
            traceback.print_exc()
            print("===============================")
            return "OCR processing failed."