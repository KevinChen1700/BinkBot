import numpy as np
import cv2
import math

def test1():
    img=cv2.imread('C:\Users\Albert\Desktop\opencv_workshop_materiaal(4)\opencv-logo-white.png')
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #BLUE COLORS
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])

    #BLUEMASK
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    res = cv2.bitwise_and(img,img, mask= mask)

    #RED COLORS
    lower_red = np.array([0,50,50])
    upper_red = np.array([10,255,255])

    #REDMASK
    maskred = cv2.inRange(hsv, lower_red, upper_red)
    resred = cv2.bitwise_and(img,img, mask= maskred)

    #GREEN COLORS
    lower_green = np.array([40,40,40])
    upper_green = np.array([70,255,255])

    #GREEN MASK
    maskgreen = cv2.inRange(hsv, lower_green, upper_green)
    resgreen = cv2.bitwise_and(img,img, mask= maskgreen)

    #Normale afbeelding
    cv2.imshow('normaal', img)
    
    #cv2.imshow('mask', mask)
    cv2.imshow('res blue',res)
    
    #cv2.imshow('maskred',maskred)
    cv2.imshow('res red',resred)

    #cv2.imshow('maskgreen',maskred)
    cv2.imshow('res green',resgreen)

    k = cv2.waitKey(0)
    print k
    cv2.destroyAllWindows()

test1()
    
