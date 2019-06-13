import os
import cv2
import imutils
import sys
import pyzbar.pyzbar as pyzbar
from collections import deque
import numpy as np
# from picamera.array import PiRGBArray
# from picamera import PiCamera
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
            # self.cap = cv2.VideoCapture(0)

    # Display barcode and QR code location
    def display(im, decodedObjects):

        # Loop over all decoded objects
        for decodedObject in decodedObjects:
            points = decodedObject.polygon

            # If the points do not form a quad, find convex hull
            if len(points) > 4:
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                hull = list(map(tuple, np.squeeze(hull)))
            else:
                hull = points;

            # Number of points in the convex hull
            n = len(hull)

            # Draw the convext hull
            for j in range(0, n):
                cv2.line(im, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)

    def qrScanner(self):

        sleep(0.1)
        self.camera.capture(stream, 'bgr', use_video_port=True)
        # stream.array now contains the image data in BGR order
        decodedObjects = pyzbar.decode(self.stream.array)
        if len(decodedObjects):
            zbarData = decodedObjects[0].data
        else:
            zbarData = ''
        if zbarData:
            cv2.putText(self.stream.array, "ZBAR : {}".format(zbarData), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0), 2)
        else:
            cv2.putText(self.stream.array, "ZBAR : QR Code NOT Detected", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 2)

        display(self.stream.array, decodedObjects)
        cv2.imshow('frame', self.stream.array)
        self.stream.seek(0)
        self.stream.truncate()
        return zbarData

    def findBlueBar(self):

        sleep(0.1)
        print("AbraKadabraAlakazam")
        # define range of blue color in HSV
        lower_blue = np.array([100, 150, 120])
        upper_blue = np.array([140, 255, 255])
        track_window = (1,1,1,1)

        ret, frame = self.cap.read()

        self.camera.capture(self.stream, 'bgr', use_video_port=True)
        blurred_frame = cv2.GaussianBlur(self.stream.array, (5, 5), 0)

        hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        roi_hist = cv2.calcHist([hsv], [0], mask, [180], [0, 180])
        cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

        # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
        term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

        contours, h = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        x = 0
        y = 0

        rect = 0, 0, 0, 0
        for contour in contours:
            rect = cv2.boundingRect(contour)

            # Deze code kan weg na testen
            x, y, w, h = rect
            track_window = (x, y, w, h)
            cv2.rectangle(self.stream.array, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # tot hier

        # Deze code kan weg na testen
        print("X: " + str(x) + " Y: " + str(y))
        if (ret == True):
            dst = cv.calcBackProject(self.stream.array, [0], roi_hist, [0, 180], 1)

            # apply meanshift to get the new location
            ret, track_window = cv2.CamShift(dst, track_window, term_crit)

            # Draw it on image
            pts = cv2.boxPoints(ret)
            pts = np.int0(pts)
            img2 = cv.polylines(self.stream.array,[pts],True, 255,2)

            cv2.drawContours(self.stream.array, contours, -1, (0, 255, 0), 3)
            # cv2.imshow("PiCamera", self.stream.array)
            #cv2.imshow("PiCamera", frame)
            # tot hier

            # reset the stream before the next capture
            self.stream.seek(0)
            self.stream.truncate()
            print("voor return")
            return frame

    def release(self):
        self.cap.release()