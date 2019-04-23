import numpy as np
import cv2
import math

cap = cv2.VideoCapture(0)
while(True):
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow('frame', hsv)

    #COLORS
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([70, 255, 255])

    green = cv2.inRange(hsv, lower_green, upper_green)

    # Morphological transformation, Dilation
    kernal = np.ones((5, 5), "uint8")
    blue = cv2.dilate(green, kernal)
    res = cv2.bitwise_and(frame, frame, mask=green)

    # Tracking Colour (Green)
    contours, hierarchy = cv2.findContours(green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > 300):
                    x, y, w, h = cv2.boundingRect(contour)
                    img = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)

    img = cv2.flip(frame, 1)
    cv2.imshow("Green", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destoryAllWindows()
