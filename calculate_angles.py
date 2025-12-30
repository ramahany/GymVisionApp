import cv2
import numpy as np
import math as m
import mediapipe as mp

from calculate_socre import front_balance_score
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Getting angles
def find_signed_angle(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    dot = dx * 0 + dy * (-1)  # dot product
    det = dx * (-1) - dy * 0  # determinant (2D cross product)

    angle_rad = m.atan2(det, dot)
    angle_deg = m.degrees(angle_rad)
    
    return angle_deg

def calculate_joint_angle(p1, p2, p3, w, h, landmarks, invert= False ):
    a = [landmarks[p1].x *w, landmarks[p1].y *h]
    b = [landmarks[p2].x *w, landmarks[p2].y *h]
    c = [landmarks[p3].x *w ,landmarks[p3].y *h]

    theta1 = find_signed_angle(b[0], b[1], a[0], a[1])
    theta2 = find_signed_angle(b[0], b[1], c[0], c[1])
    # print('theta1 = ', theta1, 'theta2 = ', theta2)
    angle = theta1 - theta2 if not invert else 360 - (theta1 - theta2)

    return angle if angle < 360 else 360 - angle

# drawing functions 

def draw_two_lines(p1, p2, p3, image, color):
    cv2.line(image, tuple([int(p1[0]), int(p1[1])]),
             tuple([int(p2[0]), int(p2[1])])
             , color, 2)
    cv2.line(image, tuple([int(p2[0]), int(p2[1])]),
             tuple([int(p3[0]), int(p3[1])])
             , color, 2)


def draw_two_lines_to_half(p1, p2, p3, image, color):
    # Convert to numpy arrays for easy math
    p1, p2, p3 = np.array(p1, dtype=np.int32), np.array(p2, dtype=np.int32), np.array(p3, dtype=np.int32)
    # Midpoints: halfway along each edge
    mid12 = (p1 + p2) / 2
    mid23 = (p2 + p3) / 2
    # Draw from midpoint → vertex
    cv2.line(image, tuple(mid12.astype(int)), tuple(p2), color, 2)
    cv2.line(image, tuple(mid23.astype(int)), tuple(p2), color, 2)
    # Draw dot at the center (p2)
    cv2.circle(image, tuple(p2), 4, color, -1)


# Specific angles and alignments (angle between leg, hips and shoulders)
def get_the_engle_between_legs(landmarks, img):# and draw it
    h, w =  img.shape[:2]

    # hips coordinates 
    left_hip = landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value]
    right_hip = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value]

    hip_center_x = (left_hip.x + right_hip.x) / 2
    hip_center_y = (left_hip.y + right_hip.y) / 2


    a = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x *w, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y *h]
    b = [hip_center_x * w, hip_center_y* h]
    c = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x *w ,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y *h]
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    color = (0,0,255)
    feed_back ='رفع الرجل الحرة عاليًا في المستوى الأفقي (زاوية 90 ْ او اكثر)'
    score = 0
    if angle >= 85: 
        color = (0,255,0)
        feed_back = ''
        score += 1 if angle < 100 else 2 
    draw_two_lines(a, b, c, img, color=color)

    return angle, score, feed_back

# Hips and shoulders 
def get_angle_between_points(x1, y1, x2, y2):
    angle_rad = m.atan2(y2 - y1, x2 - x1)
    angle_deg = m.degrees(angle_rad)
    return angle_deg


def check_hip_and_shoulders_front_balance(w_landmarks,landmarks, image, hip_min = 0, shoulder_min = 0, hip_max = 1, shoulder_max = 1):
    w, h = image.shape[:2]

    left_hip = w_landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].z 
    right_hip = w_landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].z
    
    left_shoulder = w_landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].z
    right_shoulder = w_landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].z
                      
    #checking
    check_hip = True if (hip_max > abs(right_hip-left_hip) > hip_min) else False
    check_shoulder = True if (shoulder_max > abs(right_shoulder-left_shoulder) > shoulder_min) else False
    print('check_hip', abs(right_hip-left_hip), check_hip)
    print('check_shoulder', abs(right_shoulder-left_shoulder),  check_shoulder)

    # drawing shoulder line 
    left_shoulder_draw = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    right_shoulder_draw = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

    color = (0, 255, 0) if check_shoulder else (0, 0, 255)
    cv2.line(image, tuple(np.multiply(left_shoulder_draw, [image.shape[1], image.shape[0]]).astype(int)),
             tuple(np.multiply(right_shoulder_draw, [image.shape[1], image.shape[0]]).astype(int))
             , color, 2)
    
    # drawing hip line 
    left_hip_draw = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    right_hip_draw = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
    color = (0, 255, 0) if check_hip else (0, 0, 255)
    cv2.line(image, tuple(np.multiply(left_hip_draw, [image.shape[1], image.shape[0]]).astype(int)),
             tuple(np.multiply(right_hip_draw, [image.shape[1], image.shape[0]]).astype(int))
             , color, 2)
    
    return 1 if (check_hip and check_shoulder) else 0

# analsys
def analyse_pic_front_balance(w_landmarks, landmarks, img):

    h, w =  img.shape[:2]
    score, feedback_str = 0, []
    angels = {}
    #Calculate angle between legs and the score 
    angle_between_leg, score, feed_back = get_the_engle_between_legs(landmarks, img)
    angels["angle_between_leg"] = angle_between_leg
    feedback_str.append(feed_back)

    checks = [
        ("RIGHT_KNEE", [mp_pose.PoseLandmark.RIGHT_HIP.value, mp_pose.PoseLandmark.RIGHT_KNEE.value, mp_pose.PoseLandmark.RIGHT_ANKLE.value], 170, 190, 'فرد الركبة في الرجل اليمنى', False),
        ("LEFT_HIP",[mp_pose.PoseLandmark.LEFT_SHOULDER.value, mp_pose.PoseLandmark.LEFT_HIP.value, mp_pose.PoseLandmark.LEFT_KNEE.value], 50, 185, 'رفع الجذع لاعلي', False),
        ("RIGHT_HIP",[mp_pose.PoseLandmark.RIGHT_SHOULDER.value, mp_pose.PoseLandmark.RIGHT_HIP.value, mp_pose.PoseLandmark.RIGHT_KNEE.value], 85, 160, 'ميل الجذع أماما ً في وضع موازى لألرض', True),
        ("LEFT_KNEE",[mp_pose.PoseLandmark.LEFT_HIP.value, mp_pose.PoseLandmark.LEFT_KNEE.value, mp_pose.PoseLandmark.LEFT_ANKLE.value], 170, 190, 'فرد الركبة  في الرجل اليسرى', False ),
        ("LEFT_ANKLE",[mp_pose.PoseLandmark.LEFT_KNEE.value, mp_pose.PoseLandmark.LEFT_ANKLE.value, mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value], 130, 190, 'فرد مشط القدم', True)
    ]
    

    # validation and adding angles to the dict
    for angle_name, points, min_a, max_a, fb, invert in checks:
        angle = calculate_joint_angle(*points, w, h, landmarks=landmarks, invert=invert)
        angels[angle_name] = abs(angle)
        color = (0,0,255)
        if max_a >= abs(angle) and abs(angle) >= min_a: 
            color = (0,255,0)
        else: 
            feedback_str.append(fb)
            coo = []
            for p in points: 
                coo.append([landmarks[p].x *w, landmarks[p].y *h])
            draw_two_lines_to_half(*coo, img, color)
    
    # shoulders and hips alignment 
    hips_point = check_hip_and_shoulders_front_balance(w_landmarks, landmarks,img, hip_min= 0.07 , shoulder_min=0.17)
    if not hips_point : 
        feedback_str.append('ميل الجذع في وضع موازى لألرض')
    # get score 
    score = front_balance_score(angles=angels)- (1 if not hips_point  else 0)
    return img, score, feedback_str


def analyse_pic_side_balance(w_landmarks, landmarks, img): 
# analsys
    h, w =  img.shape[:2]
    score, feedback_str = 0, []
    angels = {}
    #Calculate angle between legs and the score 
    angle_between_leg, score, feed_back = get_the_engle_between_legs(landmarks, img)
    angels["angle_between_leg"] = angle_between_leg
    feedback_str.append(feed_back)

    checks = [
        ("RIGHT_KNEE", [mp_pose.PoseLandmark.RIGHT_HIP.value, mp_pose.PoseLandmark.RIGHT_KNEE.value, mp_pose.PoseLandmark.RIGHT_ANKLE.value], 170, 190, 'فرد الركبة في الرجل اليمنى', False),
        ("LEFT_HIP",[mp_pose.PoseLandmark.LEFT_SHOULDER.value, mp_pose.PoseLandmark.LEFT_HIP.value, mp_pose.PoseLandmark.LEFT_KNEE.value], 50 , 185, 'رفع الجذع لاعلي', False),
        ("RIGHT_HIP",[mp_pose.PoseLandmark.RIGHT_SHOULDER.value, mp_pose.PoseLandmark.RIGHT_HIP.value, mp_pose.PoseLandmark.RIGHT_KNEE.value], 85, 160, 'ميل الجذع جانبـاً في وضع موازى لألرض', True),
        ("LEFT_KNEE",[mp_pose.PoseLandmark.LEFT_HIP.value, mp_pose.PoseLandmark.LEFT_KNEE.value, mp_pose.PoseLandmark.LEFT_ANKLE.value], 170, 190, 'فرد الركبة  في الرجل اليسرى', False ),
        ("LEFT_ANKLE",[mp_pose.PoseLandmark.LEFT_KNEE.value, mp_pose.PoseLandmark.LEFT_ANKLE.value, mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value], 130, 190, 'فرد مشط القدم', True)
    ]
    

    # validation and adding angles to the dict
    for angle_name, points, min_a, max_a, fb, invert in checks:
        angle = calculate_joint_angle(*points, w, h, landmarks=landmarks, invert=invert)
        angels[angle_name] = abs(angle)
        color = (0,0,255)
        if max_a >= abs(angle) and abs(angle) >= min_a: 
            color = (0,255,0)
        else: 
            feedback_str.append(fb)
            coo = []
            for p in points: 
                coo.append([landmarks[p].x *w, landmarks[p].y *h])
            draw_two_lines_to_half(*coo, img, color)
    


    # shoulders and hips alignment 
    hips_point = check_hip_and_shoulders_front_balance(w_landmarks, landmarks,img, hip_max= 0.065 , shoulder_max=0.1)
    if not hips_point : 
        feedback_str.append(" يجب ميـل الجـذع جانبـاً واسـتقامة الجـذع فـي الوضـع الجـانبي")
    
    # get score 
    score = front_balance_score(angles=angels) - (1 if not hips_point  else 0)
    return img, score, feedback_str

