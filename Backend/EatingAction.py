import os
import cv2
import time
import mediapipe as mp
from google.cloud import vision
import numpy as np
from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException

from veggiedetection import detect_veggie

# Environment setup for Google Cloud Vision
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/alexdang/Desktop/Veggieteria/Backend/veggiedetection-61937d395be7.json"

# Initialize MediaPipe Pose and Hands
eating = False
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
coin_count = 0
intervals = 0

# Initialize the connection to the Polkadot AssetHub
def init_asset_hub():
    return SubstrateInterface(
        url="wss://westmint-rpc.polkadot.io",  # Use the appropriate AssetHub endpoint
        ss58_format=42,  # Westend's ss58 prefix
        type_registry_preset='westend'
    )

# Create keypair from mnemonic
def get_keypair(mnemonic):
    return Keypair.create_from_mnemonic(mnemonic)

# Check balance
def check_balance(substrate, asset_id, address):
    result = substrate.query(
        module='Assets',
        storage_function='Account',
        params=[asset_id, address]
    )
    if result:
        return result['balance']
    return 0

# Transfer tokens
def transfer_tokens(substrate, keypair, asset_id, recipient_address, amount):
    call = substrate.compose_call(
        call_module='Assets',
        call_function='transfer',
        call_params={
            'id': asset_id,
            'target': recipient_address,
            'amount': amount
        }
    )
    extrinsic = substrate.create_signed_extrinsic(call=call, keypair=keypair)
    try:
        result = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
        return result
    except SubstrateRequestException as e:
        print(f"Failed to transfer tokens: {e}")
        return None

# Asset details
asset_id = 88228866
mnemonic = "embody vivid region bright forum clay boost horror deal escape spider path"
recipient_address = "5Gn99UhAbY2vrf59EnQD3j1WkcgpkpjcD5pRehyibNFiTqek"

# Initialize asset hub and keypair
substrate = init_asset_hub()
keypair = get_keypair(mnemonic)

# Check initial balance
initial_balance = check_balance(substrate, asset_id, recipient_address)
print(f"Initial CarrotCoin balance: {initial_balance}")

# Start video capture from the webcam
cap = cv2.VideoCapture(0)

def interval_check(start):
    global eating, coin_count, intervals
    if 3 * (intervals + 1) <= time.time() - start:
        intervals += 1
        print(f"Current coin count: {coin_count}")
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
                if distance < 0.52:  # Adjust threshold as necessary
                    eating_detected = True

    # Display the frame
    cv2.imshow('Eating Action Detection', frame)
    cv2.moveWindow('Eating Action Detection', window_x, window_y)


    if eating_detected and detect_veggie(frame):
        eating = True

    interval_check(start)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('Eating Action Detection', cv2.WND_PROP_VISIBLE) < 1:
        break

# Transfer the accumulated coins when the session ends
if coin_count > 0:
    print(f"Transferring {int(coin_count*10)} CarrotCoins to {recipient_address}")
    transfer_result = transfer_tokens(substrate, keypair, asset_id, recipient_address, int(coin_count*10))
    if transfer_result:
        print("Transfer successful:", transfer_result)
    else:
        print("Transfer failed")

# Check final balance
final_balance = check_balance(substrate, asset_id, recipient_address)
print(f"Final CarrotCoin balance: {final_balance}")

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
