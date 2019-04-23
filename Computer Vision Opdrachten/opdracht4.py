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

    hierarchy = hierarchy[0]
    for cnr in range(len(contours)):
        cnt = contours[cnr]

        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, True)
        factor = 4 * math.pi * area / perimeter**2

        holes = 0
        child = hierarchy[cnr][2]
        while child >=0:
            holes += cv2.contourArea(contours[child])
            child = hierarchy[child][0]

        print area, factor, holes

        if area > 100 and hierarchy[cnr][3] < 0:
            if factor < 0.5:
                img = cv2.drawContours(img, [cnt], -1, (0,255,255), 3) #geel
            elif factor < 0.8:
                img = cv2.drawContours(img, [cnt], -1, (0,0,255), 3) #red
            elif holes > 100:
                img = cv2.drawContours(img, [cnt], -1, (255,0,0), 3) #blauw
            else:
                img = cv2.drawContours(img, [cnt], -1, (0,255,0), 3) #groen

    #cv2.imshow('Normaal', img)
    cv2.imshow('Blur', img)
    
    k = cv2.waitKey(0)
    print k
    cv2.destroyAllWindows()

test1()
    
