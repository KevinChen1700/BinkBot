import cv2
from objectDetector import objectDetector

vision = objectDetector.getInstance()

while True:
    cv2.imshow('frame', vision.findBlueBar())
    vision.release()


    if cv2.waitKey(1) == 27:
        break





