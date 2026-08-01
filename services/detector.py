import os
from typing import List, Dict

from ultralytics import YOLO

from config import Config


class ObjectDetector:
    """
    Object Detection Service

    Uses the YOLOv8 model to detect objects in an image.
    """

    def __init__(self):
        """
        Initialize the YOLO model.
        """

        if not os.path.exists(Config.MODEL_PATH):
            raise FileNotFoundError(
                f"YOLO model not found: {Config.MODEL_PATH}"
            )

        self.model = YOLO(Config.MODEL_PATH)
        self.confidence = Config.DETECTION_CONFIDENCE

    def detect_objects(self, image_path: str) -> List[Dict]:
        """
        Detect objects in an image.

        Parameters
        ----------
        image_path : str
            Path to the image.

        Returns
        -------
        list
            List of detected objects.
        """

        if not os.path.exists(image_path):
            print(f"Image not found: {image_path}")
            return []

        try:

            predictions = self.model.predict(
                source=image_path,
                conf=self.confidence,
                save=False,
                verbose=False
            )

            detected_objects = []

            for prediction in predictions:

                for box in prediction.boxes:

                    class_id = int(box.cls[0])

                    detected_objects.append(
                        {
                            "class_name": self.model.names[class_id],
                            "confidence": round(
                                float(box.conf[0]) * 100,
                                2
                            ),
                            "bounding_box": {
                                "x1": int(box.xyxy[0][0]),
                                "y1": int(box.xyxy[0][1]),
                                "x2": int(box.xyxy[0][2]),
                                "y2": int(box.xyxy[0][3]),
                            },
                        }
                    )

            return detected_objects

        except Exception as error:

            print(f"Object Detection Error: {error}")

            return []

    def detect_object_names(self, image_path: str) -> List[str]:
        """
        Return all detected object names.
        """

        return [
            obj["class_name"]
            for obj in self.detect_objects(image_path)
        ]

    def count_objects(self, image_path: str) -> int:
        """
        Return total number of detected objects.
        """

        return len(self.detect_objects(image_path))

    def unique_objects(self, image_path: str) -> List[str]:
        """
        Return unique object names.
        """

        return sorted(
            {
                obj["class_name"]
                for obj in self.detect_objects(image_path)
            }
        )