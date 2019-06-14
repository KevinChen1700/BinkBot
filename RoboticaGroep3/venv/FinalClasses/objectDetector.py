import os
import pyzbar.pyzbar as pyzbar
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

    def findContainer(self, color):
        sleep(0.1)

        self.camera.capture(self.stream, 'bgr', use_video_port=True)

        blurred_frame = cv2.GaussianBlur(self.stream.array, (5, 5), 0)
        hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

        if color == "red":
            self.color = [0, 150, 50], [10, 255, 255], [160, 150, 50], [179, 255, 255]
            mask1 = cv2.inRange(hsv, np.array(self.color[0]), np.array(self.color[1]))

            mask2 = cv2.inRange(hsv, np.array(self.color[2]), np.array(self.color[3]))
            mask = mask1 | mask2

        if color == "blue":
            self.color = [100, 150, 0], [140, 255, 255]

        if color == "yellow":
            self.color = [23, 41, 110], [50, 255, 255]

        if color == "gray":
            self.color = [0, 10, 90], [180, 40, 160]

        # Color is not red
        if len(self.color) < 3:
            mask = cv2.inRange(hsv, np.array(self.color[0]), np.array(self.color[1]))

        contours, h = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        x = 0
        y = 0

        rect = 0, 0, 0, 0
        for contour in contours:
            rect = cv2.boundingRect(contour)
            if 200 < cv2.contourArea(contour) > 4000 and cv2.contourArea(contour) < 15000:
                x, y, w, h = rect
                cv2.rectangle(self.stream.array, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # reset the stream before the next capture
        self.stream.seek(0)
        self.stream.truncate()

        return rect

    def qrcanner(self):

        sleep(0.1)
        self.camera.capture(self.stream, 'bgr', use_video_port=True)
        # stream.array now contains the image data in BGR order
        decodedObjects = pyzbar.decode(self.stream.array)
        if len(decodedObjects):
            zbarData = decodedObjects[0].data
        else:
            zbarData = ''
        self.stream.seek(0)
        self.stream.truncate()

        return zbarData
