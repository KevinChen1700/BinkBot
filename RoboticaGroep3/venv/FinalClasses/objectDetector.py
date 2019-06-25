import os
import pyzbar.pyzbar as pyzbar
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

    #detect blue bar
    def findBlueBar(self):
        # lets the camera warm up
        sleep(0.1)
        # define range of blue color in HSV
        lower_blue = np.array([85, 120, 100])
        upper_blue = np.array([130, 255, 255])

        # start picamera recording
        self.camera.capture(self.stream, 'bgr', use_video_port=True)

        #blur and convert bgr format of video to hsv
        blurred_frame = cv2.GaussianBlur(self.stream.array, (5, 5), 0)
        hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
        #apply mask leaving only colors between the lower and upper value visible
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        #find contours in the masked frame
        contours, h = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        rect = 0, 0, 0, 0
        #apply a rectangle to every contour found
        for contour in contours:
            rect = cv2.boundingRect(contour)

        # Code to print x and y values and to display an image on screen. Is being currently used for testing
        print("X: " + str(x) + " Y: " + str(y))
        cv2.drawContours(self.stream.array, contours, -1, (0, 255, 0), 3)
        cv2.imshow("PiCamera", self.stream.array)

        # reset the stream before the next capture
        self.stream.seek(0)
        self.stream.truncate()

        #returns four values of the rectangle
        return rect

    #Detect blacklines for linedancing and eggtelligence, currently work in progress
    def blackLineDetector(self):
        sleep(0.1)

        # start picamera recording
        self.camera.capture(self.stream, 'bgr', use_video_port=True)

        index = 0
        rect = 0, 0, 0, 0
        # Height and width of image
        height = 480
        width = 640
        # Y , X
        roi = self.stream.array[height / 2:height, 0:width]

        gray = cv2.cvtColor(self.stream.array, cv2.COLOR_BGR2GRAY)
        gray = 255 - gray
        ret, thresh = cv2.threshold(gray, 250, 255, cv2.THRESH_TOZERO)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            print(cv2.contourArea(contours[index]))
            area = cv2.contourArea(contours[index])
            if area > 200 and area < 6000:
                rect = cv2.boundingRect(contour)
                # Deze code kan weg na testen
                x, y, w, h = rect
                cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.drawContours(roi, contours[index], -1, (0, 255, 0), 3)
                print(area)

        index = index + 1

    #detect colored containers for eggtelligence
    def findContainer(self, color):
        sleep(0.1)

        # start picamera recording
        self.camera.capture(self.stream, 'bgr', use_video_port=True)

        # blur and convert bgr format of video to hsv
        blurred_frame = cv2.GaussianBlur(self.stream.array, (5, 5), 0)
        hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

        #Check what color needs to be detected, based on that value it will define color range
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

        # Color is not red, because red uses two masks
        if len(self.color) < 3:
            mask = cv2.inRange(hsv, np.array(self.color[0]), np.array(self.color[1]))

        # find contours in the masked frame
        contours, h = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        x = 0
        y = 0

        rect = 0, 0, 0, 0

        # apply a rectangle to a contour if it's a certain size and store it's value in a variable
        for contour in contours:
            if 200 < cv2.contourArea(contour) > 4000 and cv2.contourArea(contour) < 15000:
                rect = cv2.boundingRect(contour)
                x, y, w, h = rect
                cv2.rectangle(self.stream.array, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # reset the stream before the next capture
        self.stream.seek(0)
        self.stream.truncate()

        # returns four values of the rectangle
        return rect

    # detect qr codes for eggtelligence
    def qrScanner(self):

        sleep(0.1)
        #start picamera recording
        self.camera.capture(self.stream, 'bgr', use_video_port=True)

        #decode the image to find the value of the qr code and store it in a variable
        decodedObjects = pyzbar.decode(self.stream.array)
        if len(decodedObjects):
            zbarData = decodedObjects[0].data
        else:
            zbarData = ''

        points = decodedObjects.polygon
        cX = (points[0].x + points[1].x + points[2].x + points[3].x) / 4
        cY = (points[0].y + points[1].y + points[2].y + points[3].y) / 4
        coordsQR = [cX, cY]
        self.stream.seek(0)
        self.stream.truncate()

        return coordsQR, zbarData
    def eggDetector(self):
        lower_white = np.array([0, 0, 180])
        upper_white = np.array([180, 200, 255])

        # code to get white from video feed
        # done before finding ellipses so finding ellipses is limited to white ones
        self.camera.capture(self.stream, 'bgr', use_video_port=True)
        blurred_frame = cv2.GaussianBlur(self.stream, (5, 5), 0)
        hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_white, upper_white)

        canny_output = cv2.Canny(mask, 255, 255 * 3)

        contours, _ = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        rect = 0, 0, 0, 0
        for i, contour in enumerate(contours):
            color = (15, (0, 256), 15, (0, 256), 15, (0, 256))
            # contour, the contour or some shit idk, it draws weird lines or some shit
            if 50 < cv2.contourArea(contour) > 400:
                #cv2.drawContours(drawing, contours, i, color)
                if contour.shape[0] > 5:
                    # ellipse, drawing the ellipses around detected shit
                    rect = cv2.boundingRect(contour)
                    # Deze code kan weg na testen
                    x, y, w, h = rect
        return rect