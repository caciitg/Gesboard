import time
import pyautogui as p
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import cv2
import numpy as np

from helper_functions import get_prediction, process_frame, process_and_extract
from helper_functions import introduce, get_diff, typechar

cap = cv2.VideoCapture(0)

(x1, y1) = (480, 100)
(x2, y2) = (790, 425)

coordinates = [(65, 335), (200, 335), (336, 335),
               (65, 415), (200, 415), (336, 415),
               (65, 490), (200, 490), (336, 490),
               (65, 565), (200, 565), (336, 565), ]

keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#']

# assume 20 frames per sec
frame_cnt = 0
click_cnt = 0


val = 1
tmp_val = "5"

keypad = cv2.imread('Images/keypad_new.png')
keypad = cv2.resize(keypad, (400, 300))


frame_thresh = 30

pre_selected = '5'
selected = '5'

# first frame for movement detection
print("Background check in progress ...")
ret, frame = cap.read()
bkgrnd = process_and_extract(frame)
ret, frame2 = cap.read()
check1 = process_and_extract(frame2)
print("Background check complete, minimum difference = ", get_diff(bkgrnd, check1))
mind = round(get_diff(bkgrnd, check1), 4)
#cv2.imshow('bk', bkgrnd)

start = 0


while True:
    ret, frame = cap.read()
    if ret:

        if not start:

            frame = np.zeros_like(process_frame(frame))
            frame = introduce(frame)
            cv2.imshow('frame', frame)

            k = cv2.waitKey(1)
            if k == ord('s'):
                start = 1

            if k == 27:
                break

            continue
            
        frame = process_frame(frame)

        extract = frame[y1:y2, x1:x2]
        diff = get_diff(bkgrnd, extract)
        momentdiff = abs(diff - mind)
        if momentdiff < 0.4:
            print("No hand")
        else:
            print("hand detected")
        

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        extract = cv2.resize(extract, (96, 96))

        frame_cnt += 1
        if frame_cnt > frame_thresh:
            # update the value every 20 frame
            val = get_prediction(extract)

            if val == 3:
                selected = keys[(keys.index(selected)+1) % 12]
            elif val == 4:
                selected = keys[((keys.index(selected)-1) % 12+12) % 12]  # talent of AT

            tmp_val = selected
            if pre_selected != selected:
                click_cnt = 0

            if val == 5:
                click_cnt += 1

            pre_selected = selected
            # print("Click count", click_cnt)
            
            if click_cnt and click_cnt%3 == 0 and val==5:
                print(f"Clicked {tmp_val} for click count {click_cnt}")
                typechar(tmp_val)            

            frame_cnt = 0

        frame = cv2.putText(frame, 
        f'{selected} : {click_cnt%3+1}/3', (90, 275), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 3)

        frame = cv2.putText(
            frame, f'{val}', (10, 25), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

        keypadch = cv2.addWeighted(
            frame[300:600, 0:400], 0.2, keypad, 0.8, 1.0)
        frame[300:600, 0:400] = keypadch

        coord = coordinates[keys.index(selected)]
        frame = cv2.circle(frame, coord, 30, (255, 255, 255), 2)

        cv2.imshow('frame', frame)

        k = cv2.waitKey(1)
        if k == 27:
            break

cap.release()
cv2.destroyAllWindows()
