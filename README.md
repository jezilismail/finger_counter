# Real-Time Finger Counter with MediaPipe & Streamlit

This project is a real-time finger counter application that uses **MediaPipe** for hand landmark detection and **Streamlit** for a live web interface.

Unlike conventional finger detection approaches that compare landmark **Y-coordinates** (for vertical fingers) and **X-coordinates** (for the thumb), this project implements a more robust and **innovative method** based on **Euclidean distance from a hand centroid**.

---

## What Makes This Project Different?

Traditional implementations check if:
- Tip's Y-coordinate is **less than** the PIP joint's Y-coordinate (i.e., finger is up).
- Thumb's X-coordinate is compared instead due to its horizontal nature.

### ⚠ Problem:
- This assumes consistent hand orientation and doesn't adapt well to hand rotations or tilted poses.

### Our Method:
1. **Find the Centroid** of key palm joints (`MCP`: 0, 1, 5, 9, 13, 17).
2. **Compute Euclidean Distance** of both the fingertip and pip joint to the centroid.
3. If the fingertip is **farther** from the centroid than its corresponding pip joint, it's considered "raised".

This method is **more reliable**, accounts for subtle rotations, and works across hand orientations.

---

## Files Explained

### `finger_detect_xy.py`
- Uses only **X** and **Y** coordinates of the landmarks.
- Suitable for 2D analysis but slightly less accurate for tilted hands or angled poses.

### `finger_detect_xyz.py`
- Extends the method to **X, Y, and Z** dimensions.
- This is more accurate, especially when hands are closer or farther from the camera.
- Forms the core logic for the Streamlit app.

### `app.py`
- A full **Streamlit app** version of the finger counter.
- Displays a **live webcam feed**.
- Shows **live finger count** in the GUI.
- Includes start/stop webcam control for user interactivity.

---

## Try the App

You can run the app locally using:

```bash
streamlit run app.py
