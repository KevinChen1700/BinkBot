import cv2
import numpy as np
import math

img = cv2.imread('C:\Users\Albert\Desktop\opencv_workshop_materiaal(4)\dobbelstenen.png')

gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

ret, th = cv2.threshold(gray,10,255,cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(th,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

eyes = []
for cnr in range(len(contours)):
    myeyes = 0;
    x, y, w, h = cv2.boundingRect(contours[cnr])
    die = gray[y:h+y, x:x+w]
    cv2.imshow('dobbelsteen' + str(cnr), die)
    ret, th2 = cv2.threshold(die,200,255,cv2.THRESH_BINARY)
    contours2, hierarchy2 = cv2.findContours(th2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for c in contours2:
        if cv2.contourArea(c) > 100 and 4 * math.pi * cv2.contourArea(c) / cv2.arcLength(c,True)**2 > 0.5:
            myeyes += 1
    eyes.append(myeyes)

eyes.sort()
print(eyes)
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
