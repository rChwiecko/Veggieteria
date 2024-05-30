import cv2
import time
import mediapipe as mp
from veggiedetection import detect_veggie

# Initialize MediaPipe Pose and Hands
eating = False
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
coin_count = 0
intervals = 0

# Start video capture from the webcam
cap = cv2.VideoCapture(0)

def interval_check(start):
    global eating, coin_count, intervals
    if 3*(intervals+1) <= time.time() - start:
       intervals += 1
       print(coin_count)
       if eating:
           coin_count += 0.1
           eating = False

# Get screen resolution
screen_width = 1920  # Replace with your screen width
screen_height = 1080  # Replace with your screen height

# Get window size
window_width = 640  # Adjust as necessary
window_height = 480  # Adjust as necessary

# Calculate the position for centering the window
window_x = int((screen_width - window_width) / 2)
window_y = int((screen_height - window_height) / 2)

# Main event loop for eating session
start = time.time()
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rgb_frame.flags.writeable = False

    # Process the frame with MediaPipe Pose and Hands
    pose_results = pose.process(rgb_frame)
    hands_results = hands.process(rgb_frame)

    # Draw pose landmarks
    rgb_frame.flags.writeable = True
    if pose_results.pose_landmarks:
        mp.solutions.drawing_utils.draw_landmarks(
            frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Draw hand landmarks and check for eating action
    eating_detected = False
    if hands_results.multi_hand_landmarks:
        for hand_landmarks in hands_results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the coordinates of the wrist (landmark 0) and thumb tip (landmark 4)
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            # Check if the thumb tip is near the mouth (landmark 9 on the pose model)
            if pose_results.pose_landmarks:
                mouth = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_LEFT]
                distance = ((wrist.x - mouth.x) ** 2 + (wrist.y - mouth.y) ** 2) ** 0.5
                if distance < 0.85:  # Adjust threshold as necessary
                    eating_detected = True

    # Display the frame
    cv2.imshow('Eating Action Detection', frame)
    cv2.moveWindow('Eating Action Detection', window_x, window_y)

    if detect_veggie(frame):
        print("veggie on screen")

    if eating_detected:
        print("eating detected")

    if eating_detected and detect_veggie(frame):
        eating = True

    interval_check(start)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('Eating Action Detection', cv2.WND_PROP_VISIBLE) < 1:
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
