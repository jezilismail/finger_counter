import streamlit as st
import cv2
import mediapipe as mp
from math import sqrt
import numpy as np
import time

import os
os.system('pip install opencv-python-headless')

# Utility functions
def get_distance(pt1, pt2):
    x1, y1, z1 = pt1
    x2, y2, z2 = pt2
    return sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 + z2)**2)

def get_centroid(pnt_list):
    MCP_points = [0, 1, 5, 9, 13, 17]
    x = y = z = 0
    for point in pnt_list:
        if point[0] in MCP_points:
            x += point[1]
            y += point[2]
            z += point[3]
    return [x / len(MCP_points), y / len(MCP_points), z / len(MCP_points)]

def hand_count(pnt_list, centroid):
    TIP_points = [4, 8, 12, 16, 20]
    count = 0
    for point in pnt_list:
        if point[0] in TIP_points:
            tip = point[1:]
            pip = pnt_list[point[0] - 2][1:]
            if get_distance(tip, centroid) > get_distance(pip, centroid):
                count += 1
    return count

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hand = mp_hands.Hands()

st.title("🖐️ Real-Time Finger Counter")

if "camera_running" not in st.session_state:
    st.session_state.camera_running = False

start = st.button("Start Webcam")
stop = st.button("Stop Webcam")

video_placeholder = st.empty()
count_placeholder = st.empty()

if start:
    st.session_state.camera_running = True

if stop:
    st.session_state.camera_running = False

# Main loop
if st.session_state.camera_running:
    cap = cv2.VideoCapture(0)

    while st.session_state.camera_running:
        ret, frame = cap.read()
        if not ret:
            break

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hand.process(img_rgb)

        count = 0
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                lm_list = []
                for i, lm in enumerate(hand_landmarks.landmark):
                    lm_list.append([i, lm.x, lm.y, lm.z])
                if len(lm_list) == 21:
                    centroid = get_centroid(lm_list)
                    count += hand_count(lm_list, centroid)
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Update Streamlit UI
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        video_placeholder.image(frame, channels="RGB")
        count_placeholder.markdown(f"### ✋ Fingers Detected: **{count}**")

        time.sleep(0.03)  # ~30 FPS

    cap.release()
    video_placeholder.empty()
    count_placeholder.markdown("Webcam stopped.")
