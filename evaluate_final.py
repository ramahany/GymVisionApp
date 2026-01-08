import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
import cv2
import numpy as np
from calculate_angles import analyse_pic_front_balance, analyse_pic_side_balance, analyse_pic_star_pose
from mediapipe.framework.formats import landmark_pb2

# model_path = 'mediapipe\models\pose_landmarker_heavy.task'
import os
# Use os.path.join for cross-platform compatibility
model_path = os.path.join('mediapipe', 'models', 'pose_landmarker_heavy.task')

# setting up mediapipe 
BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.IMAGE, 
    min_pose_detection_confidence=0.3,  # Equivalent to min_detection_confidence
    min_pose_presence_confidence=0.3)

# --- Entry Point ---
def run_check_video(frame, pose_chosen):
    resized_image = frame
    with PoseLandmarker.create_from_options(options) as landmarker:
        input_img = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=input_img)
        results = landmarker.detect(mp_image)
        if not results.pose_landmarks:
            return None
        
        drawing_spec = mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=0)
        # Define connections WITHOUT face landmarks
        connections_no_face = [
            conn for conn in mp_pose.POSE_CONNECTIONS
            if conn[0] > 10 and conn[1] > 10   # face landmarks are indices 0–10
        ]
        for pose_landmarks in results.pose_landmarks:
                # Create a NormalizedLandmarkList
                landmark_list = landmark_pb2.NormalizedLandmarkList()
                
                # Copy landmarks
                for landmark in pose_landmarks:
                    landmark_list.landmark.add(
                        x=landmark.x,
                        y=landmark.y,
                        z=landmark.z,
                        visibility=landmark.visibility
                    )
                
                # Now draw
                mp_drawing.draw_landmarks(
                    image=resized_image,
                    landmark_list=landmark_list,
                    connections=connections_no_face,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=drawing_spec
                )
        landmarks = results.pose_landmarks[0]
        w_landmarks = results.pose_world_landmarks[0]
    if pose_chosen == "star":
        return analyse_pic_star_pose(w_landmarks, landmarks, resized_image)
    
    return None
def run_check(img_path, pose_chosen):

    bytes_data = img_path.getvalue()
    image = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    # changed the way i resize the image
    height, width = image.shape[:2]
    max_dim = 800  # Max width or height
    scale = min(max_dim / width, max_dim / height)
    new_size = (int(width * scale), int(height * scale))
    resized_image = cv2.resize(image, new_size) 

    with PoseLandmarker.create_from_options(options) as landmarker:
        input_img = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=input_img)
        results = landmarker.detect(mp_image)
        if not results.pose_landmarks:
            return None
        
        drawing_spec = mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=0)
        # Define connections WITHOUT face landmarks
        connections_no_face = [
            conn for conn in mp_pose.POSE_CONNECTIONS
            if conn[0] > 10 and conn[1] > 10   # face landmarks are indices 0–10
        ]
        for pose_landmarks in results.pose_landmarks:
                # Create a NormalizedLandmarkList
                landmark_list = landmark_pb2.NormalizedLandmarkList()
                
                # Copy landmarks
                for landmark in pose_landmarks:
                    landmark_list.landmark.add(
                        x=landmark.x,
                        y=landmark.y,
                        z=landmark.z,
                        visibility=landmark.visibility
                    )
                
                # Now draw
                mp_drawing.draw_landmarks(
                    image=resized_image,
                    landmark_list=landmark_list,
                    connections=connections_no_face,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=drawing_spec
                )
        landmarks = results.pose_landmarks[0]
        w_landmarks = results.pose_world_landmarks[0]
        if pose_chosen == "front balance":
            return analyse_pic_front_balance(w_landmarks, landmarks, resized_image)
        elif pose_chosen == "side balance":
            return analyse_pic_side_balance(w_landmarks, landmarks, resized_image)
    
    return None
