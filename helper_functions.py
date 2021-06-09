import cv2
import numpy as np
import pyautogui as p
from tensorflow.keras.models import load_model
import random


print("Loading up the model...")
model = load_model('Models/KerasModelTrained_val9769_zero2five.h5')
print("Model loaded...")
(x1, y1) = (480, 100)
(x2, y2) = (790, 425)

def get_prediction(extract):
    bwsnip = cv2.cvtColor(extract, cv2.COLOR_BGR2GRAY)
    bwsnip = bwsnip.reshape((1, 96, 96, 1))
    preds = model.predict(bwsnip)
    val = np.argmax(preds[0])
    return val

def process_frame(frame):
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (800, 600))  # keep aspect ratio 1.333
    return frame


def process_and_extract(frame):
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (800, 600))  # keep aspect ratio 1.333
    return frame[y1:y2, x1:x2]


def return_bw(mat):
    return cv2.cvtColor(mat, cv2.COLOR_BGR2GRAY)


def get_diff(ext1, ext2):
    diff = np.abs(ext1 - ext2)
    mask = np.where(diff < 10, 0, 1)
    return np.sum(mask)/mask.size


def introduce(img):

    # Initialize arguments for the filter
    top = int(0.02 * img.shape[0])  # shape[0] = rows
    bottom = top
    left = int(0.02 * img.shape[1])  # shape[1] = cols
    right = left

    value = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
    borderType = cv2.BORDER_CONSTANT

    img = cv2.copyMakeBorder(img, top, bottom, left, right, borderType, None, value=[255, 0, 0])
    fontColor = (252, 254, 255)
    font = cv2.FONT_HERSHEY_SIMPLEX

    lineType = 2
    coords = (275, 125)
    fontScale = 2


    cv2.putText(img, 'Gesboard', coords, font, fontScale,fontColor, lineType)

    coords = (225, 225)
    fontScale = 1

    cv2.putText(img, 'Numpad on your fingers', coords, font, fontScale,fontColor, lineType)


    coords = (175, 300)


    cv2.putText(img, 'Use number of fingers on your hand to', coords, font,0.75,
                fontColor,lineType)

    cv2.putText(img, 'control the pointer',(300, 340),font,0.75, fontColor,
                lineType)

    cv2.putText(img, 'Place the cursor in the typing space', (200, 415), font, 0.75,
                fontColor, lineType)


    cv2.putText(img, 'and press "S" ',  (340, 455), font, 0.75,
                fontColor,  lineType)

    # Draw a rectangle with blue line borders of thickness of 2 px
    img = cv2.rectangle(img, (350, 480), (500, 600), (255, 0, 0), thickness=1)
    cv2.putText(img, '3 : move right ', (360, 510), font, 0.55, (255, 0, 0), lineType)

    cv2.putText(img, '4 : move left ', (360, 550), font, 0.55, (255, 0, 0), lineType)
    cv2.putText(img, '5 : Select ', (360, 590), font, 0.55,(255, 0, 0), lineType)

    return img


def typechar(num):
    p.keyDown(num)
    p.keyUp(num)
