# MUST be at the VERY TOP of the file
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"   # 0=all, 1=info, 2=warning, 3=error

from absl import logging
logging.set_verbosity(logging.ERROR)

# Only now import heavy libraries
import cv2
import mediapipe as mp
from typing import Dict, List


# -------------------- MediaPipe Face Detection Setup --------------------

mp_face_detection = mp.solutions.face_detection

face_detector = mp_face_detection.FaceDetection(
    model_selection=0,
    min_detection_confidence=0.5
)


# -------------------- Core Face Detection Logic --------------------

def detect_faces(frame) -> Dict:
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detector.process(image_rgb)

    faces: List[Dict] = []

    if results.detections:
        h, w, _ = frame.shape
        for detection in results.detections:
            bbox = detection.location_data.relative_bounding_box

            faces.append({
                "x": int(bbox.xmin * w),
                "y": int(bbox.ymin * h),
                "width": int(bbox.width * w),
                "height": int(bbox.height * h),
                "confidence": round(detection.score[0], 3)
            })

    return {
        "face_count": len(faces),
        "faces": faces
    }
