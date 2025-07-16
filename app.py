import mediapipe as mp
from math import sqrt
import cv2

def get_distance(pt1, pt2):
    x1, y1, z1 = pt1
    x2, y2, z2 = pt2
    dist = sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 + z2)**2)
    return dist

def get_centroid(pnt_list):
    MCP_points = [0, 1, 5, 9, 13, 17]
    MCP_len = len(MCP_points)
    x = 0
    y = 0
    z = 0
    for point in pnt_list:
        if point[0] in MCP_points:
            x += point[1]
            y += point[2]
            z += point[3]
            # print(point) # see all points take for centroid
    centroid = [x / MCP_len, y / MCP_len, z / MCP_len]
    # print(x, y, z, centroid) # see x, y, z vals and centroid 
    return centroid

def hand_count(pnt_list, centroid):
    TIP_points = [4, 8, 12, 16, 20]
    count = []
    for point in pnt_list:
        if point[0] in TIP_points:
            tip = point[1:]
            pip = pnt_list[point[0] - 2][1:]
            dist_tip = get_distance(tip, centroid)
            dist_pip = get_distance(pip, centroid)
            if dist_tip > dist_pip:
                count.append(1)
            else:
                count.append(0)
    # print(sum(count), count) # see count detection array
    return sum(count)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hand = mp_hands.Hands()

video = cv2.VideoCapture(0)

while True:
    suc, img = video.read()
    img1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hand.process(img)
    count = 0
    if result.multi_hand_landmarks:
        for hand_lmrks in result.multi_hand_landmarks:
            # print(hand_lmrks) # see full landmark data
            mp_drawing.draw_landmarks(img, hand_lmrks, mp_hands.HAND_CONNECTIONS)
            lm_list = []
    
            for id, lm in enumerate(hand_lmrks.landmark):
                # print(id, lm) # see id and landmark cords
                point_x = lm.x
                point_y = lm.y
                point_z = lm.z
                lm_list.append([id, point_x, point_y, point_z])
            
            if len(lm_list) == 21:
                # print(lm_list) # see all point values and id
                # print(img.shape) # check image w and h
                centr = get_centroid(lm_list)
                # print(centr[0], centr[1]) # see centroid x and y cords

                h, w = img.shape[:2]
                cx, cy = int(centr[0] * w), int(centr[1] * h)
                cv2.circle(img, (cx, cy), radius=3, color=(255, 0, 0), thickness=-1)

                count += hand_count(lm_list, centr)

    cv2.putText(img, f'{count}', (20, img.shape[0] - 20), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=3, color=(0, 255, 0), thickness=2)
    cv2.imshow("WEBCAM", img)
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()