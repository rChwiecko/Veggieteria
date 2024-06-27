import mediapipe as mp
import cv2
import numpy as np
import time
from mediapipe.framework.formats import landmark_pb2

# Initialize MediaPipe Face Landmarker
BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Path to the Face Landmarker model
model_path = '/Users/alexdang/Desktop/Veggieteria/Backend/experimental/face_landmarker.task'

# Callback function to handle results
def print_result(result, output_image, timestamp_ms):
    print('Face landmarks detected: {}'.format(result.face_landmarks))

# Create a face landmarker instance with the live stream mode
options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result
)

# Initialize the face landmarker
with FaceLandmarker.create_from_options(options) as landmarker:
    # Open the default camera
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert frame to RGB for MediaPipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert frame to MediaPipe Image format
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        
        # Get the timestamp in milliseconds
        frame_timestamp_ms = int(time.time() * 1000)
        
        # Perform face landmark detection asynchronously
        landmarker.detect_async(mp_image, frame_timestamp_ms)
    
    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
