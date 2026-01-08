# Behavior analysis service
import cv2
import mediapipe as mp
import numpy as np
from datetime import datetime
from typing import Dict


# -------------------- MediaPipe Setup --------------------

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=2,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


# -------------------- Behavior State --------------------

class BehaviorState:
    def __init__(self):
        self.frames_analyzed = 0
        self.no_face_frames = 0
        self.multiple_faces_frames = 0
        self.look_away_frames = 0
        self.head_movement_score = 0.0
        self.start_time = datetime.utcnow()


# -------------------- Helper Functions --------------------

def is_looking_away(landmarks) -> bool:
    """
    Determines if candidate is looking away
    based on eye landmark distance.
    """
    left_eye = landmarks[33]
    right_eye = landmarks[263]

    eye_distance = abs(left_eye.x - right_eye.x)
    return eye_distance < 0.03


def calculate_head_movement(landmarks) -> float:
    """
    Calculates head movement score using
    nose-to-chin distance variance.
    """
    nose_tip = landmarks[1]
    chin = landmarks[152]

    return abs(nose_tip.y - chin.y)


# -------------------- Core Analyzer --------------------

def analyze_frame(frame: np.ndarray, state: BehaviorState) -> None:
    """
    Analyze a single video frame and update behavior state.
    """
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb_frame)

    state.frames_analyzed += 1

    if not result.multi_face_landmarks:
        state.no_face_frames += 1
        return

    if len(result.multi_face_landmarks) > 1:
        state.multiple_faces_frames += 1
        return

    landmarks = result.multi_face_landmarks[0].landmark

    if is_looking_away(landmarks):
        state.look_away_frames += 1

    state.head_movement_score += calculate_head_movement(landmarks)


# -------------------- Final Report --------------------

def generate_behavior_report(state: BehaviorState) -> Dict:
    """
    Generate final behavior analytics report.
    """
    duration_sec = (datetime.utcnow() - state.start_time).seconds
    total_frames = max(1, state.frames_analyzed)

    return {
        "duration_seconds": duration_sec,
        "frames_analyzed": state.frames_analyzed,
        "no_face_ratio": round(state.no_face_frames / total_frames, 3),
        "multiple_faces_ratio": round(state.multiple_faces_frames / total_frames, 3),
        "look_away_ratio": round(state.look_away_frames / total_frames, 3),
        "head_movement_score": round(state.head_movement_score, 2),
        "behavior_flag": state.look_away_frames > (0.3 * total_frames)
    }
