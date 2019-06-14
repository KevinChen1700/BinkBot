from objectDetector import objectDetector
import cv2
import numpy as np


vision = objectDetector.getInstance()

vision.findContainer("yellow")