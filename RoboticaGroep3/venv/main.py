import numpy as np
import cv2
import math
from Motor import Motor


def test1():
    img = cv2.imread('img/download.jpg')
    cv2.imshow('logo', img)
    k = cv2.waitKey(0)
    print k
    cv2.destroyAllWindows()

def Testfunctie():
    motor1 = Motor(1, 2, 3)
    testreturn = motor1.getTest()
    return testreturn

print (Testfunctie())