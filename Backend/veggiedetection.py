import os
import cv2
from google.cloud import vision
import numpy as np

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/sauce/Veggieteria/Backend/veggiedetection-61937d395be7.json"

def detect_veggie(image_frame):
    """Detects labels in the image frame and checks for the presence of vegetables."""
    client = vision.ImageAnnotatorClient()

    # Convert the image frame (ndarray) to bytes
    _, encoded_image = cv2.imencode('.png', image_frame)
    content = encoded_image.tobytes()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    # List of labels to check for
    vegetable_labels = ['vegetable', 'carrot', 'broccoli', 'lettuce', 'tomato', 'pepper', 'cucumber', 'spinach', 'cabbage', 'onion']

    for label in labels:
        if any(veg in label.description.lower() for veg in vegetable_labels):
            return True

    return False