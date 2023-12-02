import cv2
import numpy as np
import math

import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

square_x = 100
square_y = 100
square_width = 100
square_color = (255,0,0)
L1 = 0
L2 = 0
on_square = False

while True:

    ret,frame = cap.read()

    frame = cv2.flip(frame,1)

    frame.flags.writeable = False
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results = hands.process(frame)

    frame.flags.writeable = True
    frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )
        x_list = []
        y_list = []
        for landmark in hand_landmarks.landmark:
            x_list.append(landmark.x)
            y_list.append(landmark.y)

        index_finger_x = int(x_list[8] * width)
        index_finger_y = int(y_list[8] * height)

        meddle_finger_x = int(x_list[12] * width)
        meddle_finger_y = int(y_list[12] * height)

        finger_len = math.hypot((index_finger_x-meddle_finger_x),(index_finger_y-meddle_finger_y))

        if finger_len < 30:
            if (index_finger_x > square_x) and (index_finger_x <(square_x+square_width)):
                if (index_finger_y > square_y) and (index_finger_y<(square_y+square_width)):
                    L1 - abs(index_finger_x - square_x)
                    L2 = abs(index_finger_y - square_y)
                    on_square = True
                    

            if on_square == True:
                square_x = index_finger_x - L1
                square_y = index_finger_y - L2
                square_color = (0,0,255)

        else:
            on_square = False
            square_color = (255,0,0)

    # cv2.rectangle(frame,(square_x,square_y),(square_x+square_width,
    # square_y+square_width),(255,0,0),-1)

    overlay = frame.copy()
    cv2.rectangle(frame,(square_x,square_y),(square_x+
    square_width,square_y+square_width),square_color,-1)
    frame = cv2.addWeighted(overlay,0.5,frame,0.5,0)

    cv2.imshow("Virtual drag",frame)

    if cv2.waitKey(10) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()