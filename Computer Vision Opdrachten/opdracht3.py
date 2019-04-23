import numpy as np
import cv2
import math

def test1():
    img=cv2.imread('C:/Users/Albert/Desktop/opencv_workshop_materiaal(4)/bouten_moeren.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)

    ret, th = cv2.threshold(blur, 180,255,cv2.THRESH_BINARY_INV)
    cv2.findContours(th,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    contours, hierarchy = cv2.findContours(th,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 100:
            blur = cv2.drawContours(img, [cnt], -1, (0,255,255), 3)
    
    #cv2.imshow('Normaal', img)
    cv2.imshow('Blur', blur)
    
    k = cv2.waitKey(0)
    print k
    cv2.destroyAllWindows()

test1()
    
