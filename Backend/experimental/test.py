import mediapipe as mp
import cv2
import time
# Initialize MediaPipe and the face detector with custom model
BaseOptions = mp.tasks.BaseOptions
FaceDetector = mp.tasks.vision.FaceDetector
FaceDetectorOptions = mp.tasks.vision.FaceDetectorOptions
FaceDetectorResult = mp.tasks.vision.FaceDetectorResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Callback function to handle results
def print_result(result: FaceDetectorResult, output_image: mp.Image, timestamp_ms: int):
    print(f'Face detector result at {timestamp_ms} ms: {result}')

options = FaceDetectorOptions(
    base_options=BaseOptions(model_asset_path='/Users/alexdang/Veggieteria/Backend/experimental/blaze_face_short_range.tflite'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result
)

# Initialize the face detector
detector = FaceDetector.create_from_options(options)

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

    # Perform face detection asynchronously
    detector.detect_async(mp_image, frame_timestamp_ms)

    # Display the frame
    cv2.imshow('Face Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit loop on 'q' key press
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

# Clean up the detector
detector.close()
