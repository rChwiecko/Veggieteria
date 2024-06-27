import mediapipe as mp
import cv2
import numpy as np

# Initialize MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Define a function to extract mouth landmarks
def extract_mouth_landmarks(face_landmarks):
    mouth_indices = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 61]
    mouth_landmarks = []
    for idx in mouth_indices:
        landmark = face_landmarks.landmark[idx]
        mouth_landmarks.append((landmark.x, landmark.y, landmark.z))
    return mouth_landmarks

# Define a function to calculate the distance between points
def calculate_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Define a function to determine if the mouth is open
def is_mouth_open(mouth_landmarks):
    upper_lip = np.mean([mouth_landmarks[i] for i in [0, 1, 2, 3, 4]], axis=0)
    lower_lip = np.mean([mouth_landmarks[i] for i in [7, 8, 9, 10, 11]], axis=0)
    distance = calculate_distance(upper_lip, lower_lip)
    return distance > 0.03  # Adjust the threshold as needed

# Open the default camera
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe FaceMesh
    results = face_mesh.process(frame_rgb)

    # Draw landmarks and detect eating action
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Draw the face mesh
            mp_drawing.draw_landmarks(
                frame,
                face_landmarks,
                mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
            )

            # Extract mouth landmarks
            mouth_landmarks = extract_mouth_landmarks(face_landmarks)

            # Check if the mouth is open
            if is_mouth_open(mouth_landmarks):
                cv2.putText(frame, 'Eating Detected', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Facial Landmarks Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

# Clean up the face mesh
face_mesh.close()
