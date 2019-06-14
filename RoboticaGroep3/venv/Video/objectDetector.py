import os
import cv2
import numpy as np
#from picamera.array import PiRGBArray
#from picamera import PiCamera
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
           # self.camera = PiCamera()
            #self.camera.resolution = (640, 480)
            #self.camera.framerate = 90
            #self.stream = PiRGBArray(self.camera, size=(640, 480))
            self.cap = cv2.VideoCapture(0)
            self.red = [0, 150,150], [10, 255, 255]
            self.color = 0


