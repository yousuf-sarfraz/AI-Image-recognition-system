import logging
import os
from typing import Dict, List

from ultralytics import YOLO

from config import Config


logger = logging.getLogger(__name__)


class ObjectDetector:
    """
    Object Detection Service

    Uses the YOLO model to detect objects in images.
    """

    def __init__(self):
        """
        Initialize the YOLO model and detection settings.
        """

        model_path = Config.MODEL_PATH

        # Check whether the model exists
        if not os.path.isfile(model_path):
            raise FileNotFoundError(
                f"YOLO model not found: {model_path}"
            )

        try:
            self.model = YOLO(model_path)
            self.confidence = Config.DETECTION_CONFIDENCE

            logger.info(
                "YOLO model loaded successfully: %s",
                model_path,
            )

        except Exception:
            logger.exception(
                "Failed to load YOLO model: %s",
                model_path,
            )
            raise

    def detect_objects(self, image_path: str) -> List[Dict]:
        """
        Detect objects in an image.

        Parameters
        ----------
        image_path : str
            Path to the image.

        Returns
        -------
        List[Dict]
            List containing detected object information.
        """

        # Check whether image exists
        if not os.path.isfile(image_path):
            logger.warning(
                "Image not found: %s",
                image_path,
            )
            return []

        try:
            # Run YOLO prediction
            predictions = self.model.predict(
                source=image_path,
                conf=self.confidence,
                imgsz=Config.IMAGE_SIZE,
                save=False,
                verbose=False,
            )

            detected_objects: List[Dict] = []

            # Process prediction results
            for prediction in predictions:

                if prediction.boxes is None:
                    continue

                for box in prediction.boxes:

                    class_id = int(box.cls[0])

                    confidence = float(box.conf[0])

                    coordinates = box.xyxy[0].tolist()

                    x1, y1, x2, y2 = map(
                        int,
                        coordinates
                    )

                    detected_objects.append(
                        {
                            "class_name": self.model.names[class_id],

                            "confidence": round(
                                confidence * 100,
                                2
                            ),

                            "bounding_box": {
                                "x1": x1,
                                "y1": y1,
                                "x2": x2,
                                "y2": y2,
                            },
                        }
                    )

            logger.info(
                "Detected %d object(s) in %s",
                len(detected_objects),
                image_path,
            )

            return detected_objects

        except Exception:
            logger.exception(
                "Object detection failed for: %s",
                image_path,
            )

            return []

    def detect_object_names(self, image_path: str) -> List[str]:
        """
        Return the names of all detected objects.
        """

        objects = self.detect_objects(image_path)

        return [
            obj["class_name"]
            for obj in objects
        ]

    def count_objects(self, image_path: str) -> int:
        """
        Return the total number of detected objects.
        """

        return len(
            self.detect_objects(image_path)
        )

    def unique_objects(self, image_path: str) -> List[str]:
        """
        Return unique detected object names.
        """

        objects = self.detect_objects(image_path)

        return sorted(
            {
                obj["class_name"]
                for obj in objects
            }
        )