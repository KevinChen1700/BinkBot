import os
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import sys
from time import sleep


class ObjectDetector:
    __instance = None
    @staticmethod
    def getInstance():  # function to get the only instance of this class since the class is a singleton
        # if there isn't an instance of this class yet, create it
        if ObjectDetector.__instance is None:
            ObjectDetector()
        # return this class's only instance
        return objectDetector.__instance

    def __init__(self):
        if ObjectDetector.__instance is not None:  # if the constructor of this class is called more than once
            raise Exception("This class is a singleton!")
        else:
            # puts the created instance in the "__instance" variable
            ObjectDetector.__instance = self
            # creates a PiCamera instance to take pictures
            self.camera = PiCamera()
            self.camera.resolution = (640, 480)
            self.camera.framerate = 90
            self.stream = PiRGBArray(self.camera, size=(640, 480))

    def findBlueBar(self):
        # lets the camera warm up
        sleep(0.1)
        # define range of blue color in HSV
        lower_blue = np.array([85, 120, 100])
        upper_blue = np.array([130, 255, 255])

        # takes a picture
        self.camera.capture(self.stream, 'bgr', use_video_port=True)

        # blurs the picture to remove noise
        blurred_frame = cv2.GaussianBlur(self.stream.array, (5, 5), 0)
        hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)  # converts the picture to hsv
        # only leaves colors that are between lower and upper_blue in hsv values in the image
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        contours, h = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        rect = 0, 0, 0, 0
        for contour in contours:
            rect = cv2.boundingRect(contour)

        # reset the stream before the next capture
        self.stream.seek(0)
        self.stream.truncate()

        return rect
