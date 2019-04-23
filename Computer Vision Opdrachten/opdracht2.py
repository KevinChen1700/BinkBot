import numpy as np
import cv2
import math

def test1():
    img=cv2.imread('C:\Users\Albert\Desktop\opencv_workshop_materiaal(4)\opencv-logo-white.png')
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #RED COLORS
    lower_red = np.array([0,50,50])
    upper_red = np.array([10,255,255])

    #REDMASK
    maskred = cv2.inRange(hsv, lower_red, upper_red)

    contours,hierarchy = cv2.findContours(maskred,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        M = cv2.moments(cnt)
        if M['m00'] > 1000:
            cnt = cv2.convexHull(cnt[0])
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

    cnt2 = cv2.convexHull(contours[0])
    img = cv2.drawContours(img, [cnt2], -1, (0,255,255), 3)
    img = cv2.circle(img, (cx,cy), 5, (0,255,255), -1)

    
    cv2.imshow('Countours', img)
    k = cv2.waitKey(0)
    print k
    cv2.destroyAllWindows()

test1()
    
