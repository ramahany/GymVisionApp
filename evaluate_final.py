import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
import cv2
import numpy as np
from calculate_angles import analyse_pic_front_balance, analyse_pic_side_balance

# --- Entry Point ---
def run_check(img_path, pose_chosen):
    bytes_data = img_path.getvalue()
    image = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
 
    # changed the way i resize the image
    
    # TODO change the width and the hight of the displayed image and make it so it fits the model
    height, width = image.shape[:2]
    max_dim = 800  # Max width or height
    scale = min(max_dim / width, max_dim / height)
    new_size = (int(width * scale), int(height * scale))
    resized_image = cv2.resize(image, new_size)
    print(resized_image.shape)
    with mp_pose.Pose(static_image_mode=True, 
                      min_detection_confidence=0.5) as pose:
        input_img = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        results = pose.process(input_img)

        if not results.pose_landmarks:
            return None
        
        drawing_spec = mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=0)
        # Define connections WITHOUT face landmarks
        connections_no_face = [
            conn for conn in mp_pose.POSE_CONNECTIONS
            if conn[0] > 10 and conn[1] > 10   # face landmarks are indices 0–10
        ]
        mp_drawing.draw_landmarks(
            image=resized_image,
            landmark_list=results.pose_landmarks,
            connections=connections_no_face,
            landmark_drawing_spec=None,
            connection_drawing_spec=drawing_spec
        )
        landmarks = results.pose_landmarks.landmark
        w_landmarks = results.pose_world_landmarks.landmark
        if pose_chosen == "front balance":
            return analyse_pic_front_balance(w_landmarks, landmarks, resized_image)
        elif pose_chosen == "side balance":
            return analyse_pic_side_balance(w_landmarks, landmarks, resized_image)

    return None
