import mediapipe as mp
import cv2
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime
import math
import warnings
import pickle
import csv
import os
import json
import tensorflow as tf
import time

warnings.filterwarnings('ignore')



##########################################################################################################################################

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False  
    
    results = model.process(image)
    
    image.flags.writeable = True                  
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) 
    
    return image, results

def draw_landmarks(image, results):
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=1, circle_radius=1),
                              mp_drawing.DrawingSpec(color=(208, 224, 65), thickness=2, circle_radius=1))
    
def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    return pose

actions = np.array(['bicep_curls', 'planks', 'squats'])

##########################################################################################################################################
##################################################   BICEPS #################################################################

IMPORTANT_LMS_bicep_curls = [
    "NOSE",
    "LEFT_SHOULDER",
    "RIGHT_SHOULDER",
    "RIGHT_ELBOW",
    "LEFT_ELBOW",
    "RIGHT_WRIST",
    "LEFT_WRIST",
    "LEFT_HIP",
    "RIGHT_HIP",
]

# Generate all columns of the data frame

HEADERS_bicep_curls = ["label"]  # Label column

for lm in IMPORTANT_LMS_bicep_curls:
    HEADERS_bicep_curls += [f"{lm.lower()}_x", f"{lm.lower()}_y",
                f"{lm.lower()}_z", f"{lm.lower()}_v"]


def calculate_angle(point1: list, point2: list, point3: list) -> float:
    '''
    Calculate the angle between 3 points
    Unit of the angle will be in Degree
    '''
    point1 = np.array(point1)
    point2 = np.array(point2)
    point3 = np.array(point3)

    # Calculate algo
    angleInRad = np.arctan2(point3[1] - point2[1], point3[0] - point2[0]) - \
        np.arctan2(point1[1] - point2[1], point1[0] - point2[0])
    angleInDeg = np.abs(angleInRad * 180.0 / np.pi)

    angleInDeg = angleInDeg if angleInDeg <= 180 else 360 - angleInDeg
    return angleInDeg


def extract_important_keypoints_bicep_curls(results, important_landmarks: list) -> list:
    '''
    Extract important keypoints from mediapipe pose detection
    '''
    landmarks = results.pose_landmarks.landmark

    data = []
    for lm in important_landmarks:
        keypoint = landmarks[mp_pose.PoseLandmark[lm].value]
        data.append([keypoint.x, keypoint.y, keypoint.z, keypoint.visibility])

    return np.array(data).flatten().tolist()


# Load input scaler
with open("./exe_final/bicep/input_scaler.pkl", "rb") as f:
    bicep_curls_input_scaler = pickle.load(f)

# Load model
with open("./exe_final/bicep/KNN_model.pkl", "rb") as f:
    bicep_curls_sklearn_model = pickle.load(f)


class BicepPoseAnalysis:
    def __init__(self, side: str, stage_down_threshold: float, stage_up_threshold: float, peak_contraction_threshold: float, loose_upper_arm_angle_threshold: float, visibility_threshold: float):
        self.stage_down_threshold = stage_down_threshold
        self.stage_up_threshold = stage_up_threshold
        self.peak_contraction_threshold = peak_contraction_threshold
        self.loose_upper_arm_angle_threshold = loose_upper_arm_angle_threshold
        self.visibility_threshold = visibility_threshold

        self.side = side
        self.counter = 0
        self.stage = "down"
        self.is_visible = True
        self.detected_errors = {
            "LOOSE_UPPER_ARM": 0,
            "PEAK_CONTRACTION": 0,
        }

        self.loose_upper_arm = False

        self.peak_contraction_angle = 1000
        self.peak_contraction_frame = None

    def record_to_json(self, file_name):
        # Generate today's date string in the format YYYY-MM-DD
        today_date = datetime.now().strftime("%Y-%m-%d")

        try:
            # Load existing data from the JSON file
            with open(file_name, "r") as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            # If the file does not exist, initialize an empty data dictionary
            data = {}

        # Check if "biceps" key exists in the data dictionary
        if "biceps" not in data:
            data["biceps"] = {"left": [], "right": [], 'lb_error':[]}

        # Create a dictionary for the current set data
        set_data = {
            "lua": self.detected_errors["LOOSE_UPPER_ARM"],
            "pc": self.detected_errors["PEAK_CONTRACTION"],
            "reps": self.counter
        }

        # Append the set data to the list corresponding to the current side
        if self.side == "left":
            data["biceps"]["left"].append(set_data)
        elif self.side == "right":
            data["biceps"]["right"].append(set_data)

        # Add the lean back error count to the data dictionary
        data["biceps"]["lb_error"].append(lean_back_error_count)

        # Write the updated data back to the JSON file
        with open(file_name, "w") as json_file:
            json.dump(data, json_file, indent=4)

    def get_joints(self, landmarks) -> bool:
        '''
        Check for joints' visibility then get joints coordinate
        '''
        side = self.side.upper()

        joints_visibility = [landmarks[mp_pose.PoseLandmark[f"{side}_SHOULDER"].value].visibility, landmarks[
            mp_pose.PoseLandmark[f"{side}_ELBOW"].value].visibility, landmarks[mp_pose.PoseLandmark[f"{side}_WRIST"].value].visibility]

        is_visible = all(
            [vis > self.visibility_threshold for vis in joints_visibility])
        self.is_visible = is_visible

        if not is_visible:
            return self.is_visible

        self.shoulder = [landmarks[mp_pose.PoseLandmark[f"{side}_SHOULDER"].value].x,
                         landmarks[mp_pose.PoseLandmark[f"{side}_SHOULDER"].value].y]
        self.elbow = [landmarks[mp_pose.PoseLandmark[f"{side}_ELBOW"].value].x,
                      landmarks[mp_pose.PoseLandmark[f"{side}_ELBOW"].value].y]
        self.wrist = [landmarks[mp_pose.PoseLandmark[f"{side}_WRIST"].value].x,
                      landmarks[mp_pose.PoseLandmark[f"{side}_WRIST"].value].y]

        return self.is_visible

    def analyze_pose(self, landmarks, frame):
        '''
        - Bicep Counter
        - Errors Detection
        '''
        self.get_joints(landmarks)

        # Cancel calculation if visibility is poor
        if not self.is_visible:
            return (None, None)

        bicep_curl_angle = int(calculate_angle(
            self.shoulder, self.elbow, self.wrist))
        if bicep_curl_angle > self.stage_down_threshold:
            self.stage = "down"
        elif bicep_curl_angle < self.stage_up_threshold and self.stage == "down":
            self.stage = "up"
            self.counter += 1

        # Represent the projection of the shoulder to the X axis
        shoulder_projection = [self.shoulder[0], 1]
        ground_upper_arm_angle = int(calculate_angle(
            self.elbow, self.shoulder, shoulder_projection))

        if ground_upper_arm_angle > self.loose_upper_arm_angle_threshold:
            # Limit the saved frame
            if not self.loose_upper_arm:
                self.loose_upper_arm = True
                # save_frame_as_image(frame, f"Loose upper arm: {ground_upper_arm_angle}")
                self.detected_errors["LOOSE_UPPER_ARM"] += 1
        else:
            self.loose_upper_arm = False

        if self.stage == "up" and bicep_curl_angle < self.peak_contraction_angle:
            self.peak_contraction_angle = bicep_curl_angle
            self.peak_contraction_frame = frame

        elif self.stage == "down":
            if self.peak_contraction_angle != 1000 and self.peak_contraction_angle >= self.peak_contraction_threshold:
                self.detected_errors["PEAK_CONTRACTION"] += 1

            self.peak_contraction_angle = 1000
            self.peak_contraction_frame = None

        return (bicep_curl_angle, ground_upper_arm_angle)
    
    
##########################################################################################################################################
##################################################   analysis functions #################################################################

def analyze_bicep_curls(image, results):
    global posture, lean_back_error_count, prev_post
    try:
        landmarks = results.pose_landmarks.landmark  
        
        (left_bicep_curl_angle, left_ground_upper_arm_angle) = left_arm_analysis.analyze_pose(landmarks=landmarks, frame=image)
        (right_bicep_curl_angle, right_ground_upper_arm_angle) = right_arm_analysis.analyze_pose(landmarks=landmarks, frame=image)
  
        row = extract_important_keypoints_bicep_curls(results, IMPORTANT_LMS_bicep_curls)
        X = pd.DataFrame([row], columns=HEADERS_bicep_curls[1:])
        X = pd.DataFrame(bicep_curls_input_scaler.transform(X))
        
        predicted_class = bicep_curls_sklearn_model.predict(X)[0]
        prediction_probabilities = bicep_curls_sklearn_model.predict_proba(X)[0]
        class_prediction_probability = round(prediction_probabilities[np.argmax(prediction_probabilities)], 2)

        if class_prediction_probability >= POSTURE_ERROR_THRESHOLD:
            posture = predicted_class

        if posture == "L" and posture != prev_post:
            lean_back_error_count += 1
        prev_post = posture
     
    except Exception as e:
        print(f"Error: {e}")

    return (right_arm_analysis.detected_errors["PEAK_CONTRACTION"],
            right_arm_analysis.detected_errors["LOOSE_UPPER_ARM"],
            left_arm_analysis.detected_errors["PEAK_CONTRACTION"],
            left_arm_analysis.detected_errors["LOOSE_UPPER_ARM"],
            lean_back_error_count,
            left_arm_analysis.counter)    
        

        
    

##########################################################################################################################################
##################################################   INFERENCE #################################################################

VISIBILITY_THRESHOLD = 0.65
STAGE_UP_THRESHOLD = 90
STAGE_DOWN_THRESHOLD = 120
POSTURE_ERROR_THRESHOLD = 0.85
PEAK_CONTRACTION_THRESHOLD = 25
LOOSE_UPPER_ARM = False
LOOSE_UPPER_ARM_ANGLE_THRESHOLD = 20
lean_back_error_count = 0
prev_post = None
posture = None


left_arm_analysis = BicepPoseAnalysis(side="left", stage_down_threshold=STAGE_DOWN_THRESHOLD, stage_up_threshold=STAGE_UP_THRESHOLD,
                                      peak_contraction_threshold=PEAK_CONTRACTION_THRESHOLD, loose_upper_arm_angle_threshold=LOOSE_UPPER_ARM_ANGLE_THRESHOLD, visibility_threshold=VISIBILITY_THRESHOLD)

right_arm_analysis = BicepPoseAnalysis(side="right", stage_down_threshold=STAGE_DOWN_THRESHOLD, stage_up_threshold=STAGE_UP_THRESHOLD,
                                       peak_contraction_threshold=PEAK_CONTRACTION_THRESHOLD, loose_upper_arm_angle_threshold=LOOSE_UPPER_ARM_ANGLE_THRESHOLD, visibility_threshold=VISIBILITY_THRESHOLD)



