 #!/usr/bin/env python
import cv2
import dlib
import imutils
import numpy as np
from imutils.video import VideoStream
from imutils import face_utils
import time
import serial
from EAR import eye_aspect_ratio
from MAR import mouth_aspect_ratio
from HeadPose import getHeadTiltAndCoords

# -------------------- Serial Setup --------------------
try:
    esp32 = serial.Serial('COM6', 115200, timeout=1)
    time.sleep(2)
    print("[INFO] Connected to ESP32 on COM6")
except Exception as e:
    esp32 = None
    print("[WARNING] Could not connect to ESP32:", e)

# -------------------- Initialize dlib --------------------
print("[INFO] Loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('./dlib_shape_predictor/shape_predictor_68_face_landmarks.dat')

print("[INFO] Initializing camera...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

frame_width = 1024
frame_height = 576

# Head pose key points
image_points = np.array([
    (359, 391), (399, 561), (337, 297),
    (513, 301), (345, 465), (453, 469)
], dtype="double")

# Facial landmark index ranges
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(mStart, mEnd) = (49, 68)

# -------------------- Thresholds --------------------
EYE_AR_THRESH = 0.25
MOUTH_AR_THRESH = 0.79
HEAD_TILT_THRESH = 30
EYE_AR_CONSEC_FRAMES = 3

# -------------------- Counters --------------------
COUNTER = 0
DANGER_COUNTER = 0
SAFE_COUNTER = 0

DANGER_FRAMES = 10   # Require 10 continuous danger frames
SAFE_FRAMES = 5      # Require 5 safe frames to reset

status = "SAFE"
last_status = ""

# -------------------- Main Loop --------------------
while True:
    frame = vs.read()
    if frame is None:
        print("[ERROR] Could not read frame!")
        break

    frame = imutils.resize(frame, width=frame_width, height=frame_height)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)

    danger_detected = False

    for rect in rects:
        (bX, bY, bW, bH) = face_utils.rect_to_bb(rect)
        cv2.rectangle(frame, (bX, bY), (bX + bW, bY + bH), (0, 255, 0), 1)

        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # -------- EAR (Eye Aspect Ratio) --------
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0

        if ear < EYE_AR_THRESH:
            COUNTER += 1
            if COUNTER >= EYE_AR_CONSEC_FRAMES:
                cv2.putText(frame, "Eyes Closed!", (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                danger_detected = True
        else:
            COUNTER = 0

        # -------- MAR (Yawning) --------
        mouth = shape[mStart:mEnd]
        mar = mouth_aspect_ratio(mouth)

        if mar > MOUTH_AR_THRESH:
            cv2.putText(frame, "Yawning!", (650, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            danger_detected = True

        # -------- Head Tilt --------
        for (i, (x, y)) in enumerate(shape):
            if i == 33: image_points[0] = np.array([x, y], dtype='double')
            elif i == 8: image_points[1] = np.array([x, y], dtype='double')
            elif i == 36: image_points[2] = np.array([x, y], dtype='double')
            elif i == 45: image_points[3] = np.array([x, y], dtype='double')
            elif i == 48: image_points[4] = np.array([x, y], dtype='double')
            elif i == 54: image_points[5] = np.array([x, y], dtype='double')

        (head_tilt_degree, start_point, end_point, end_point_alt) = getHeadTiltAndCoords(
            gray.shape, image_points, frame_height)

        if head_tilt_degree:
            tilt = abs(head_tilt_degree[0])
            if tilt > HEAD_TILT_THRESH:
                cv2.putText(frame, "Head Tilt!", (20, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                danger_detected = True

    # -------- Stability Logic --------
    if danger_detected:
        DANGER_COUNTER += 1
        SAFE_COUNTER = 0
    else:
        SAFE_COUNTER += 1
        DANGER_COUNTER = 0

    # Decide final status
    if DANGER_COUNTER >= DANGER_FRAMES:
        status = "DANGER"
    elif SAFE_COUNTER >= SAFE_FRAMES:
        status = "SAFE"

    # Display status
    if status == "DANGER":
        cv2.putText(frame, "DROWSINESS ALERT", (300, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    else:
        cv2.putText(frame, "Driver Safe", (300, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    # -------- Send to ESP32 (only on change) --------
    if status != last_status and esp32:
        esp32.write((status + "\n").encode())
        print(f"Sent to ESP32: {status}")
        last_status = status

    # -------- Show Frame --------
    cv2.imshow("Driver Monitoring", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# -------------------- Cleanup --------------------
cv2.destroyAllWindows()
vs.stop()
if esp32:
    esp32.close()
