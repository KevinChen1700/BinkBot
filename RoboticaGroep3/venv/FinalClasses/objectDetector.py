import os
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import sys
from time import sleep
class objectDetector:
    __instance = None

    @staticmethod
    def getInstance():
        if objectDetector.__instance is None:
            objectDetector()
        return objectDetector.__instance

    def __init__(self):
        if objectDetector.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            objectDetector.__instance = self
            self.camera = PiCamera()
            self.camera.resolution = (640, 480)
            self.camera.framerate = 90
            self.stream = PiRGBArray(self.camera, size=(640, 480))

    def findBlueBar(self):
        sleep(0.1)
        print("AbraKadabraAlakazam")
        # define range of blue color in HSV
        lower_blue = np.array([100, 150, 120])
        upper_blue = np.array([140, 255, 255])

        self.camera.capture(self.stream, 'bgr', use_video_port=True)

        blurred_frame = cv2.GaussianBlur(self.stream.array, (5, 5), 0)
        hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        contours, h = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        x = 0
        y = 0

        rect = 0, 0, 0, 0
        for contour in contours:
            rect = cv2.boundingRect(contour)

            # Deze code kan weg na testen
            x, y, w, h = rect
            cv2.rectangle(self.stream.array, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # tot hier

        # Deze code kan weg na testen
        print("X: " + str(x) + " Y: " + str(y))
        cv2.drawContours(self.stream.array, contours, -1, (0, 255, 0), 3)
        cv2.imshow("PiCamera", self.stream.array)
        # tot hier


        # reset the stream before the next capture
        self.stream.seek(0)
        self.stream.truncate()

        return rect
