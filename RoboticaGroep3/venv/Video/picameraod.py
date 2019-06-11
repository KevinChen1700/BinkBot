######## Picamera Object Detection Using Tensorflow Classifier #########
#
# Author: Evan Juras
# Date: 4/15/18
# Description: 
# This program uses a TensorFlow classifier to perform object detection.
# It loads the classifier uses it to perform object detection on a Picamera feed.
# It draws boxes and scores around the objects of interest in each frame from
# the Picamera. It also can be used with a webcam by adding "--usbcam"
# when executing this script from the terminal.

## Some of the code is copied from Google's example at
## https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb

## and some is copied from Dat Tran's example at
## https://github.com/datitran/object_detector_app/blob/master/object_detection_app.py

## but I changed it to make it more understandable to me.


# Import packages
import os
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import tensorflow as tf
import argparse
import sys
from time import sleep

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 90
stream = PiRGBArray(camera, size=(640, 480))

#Function to test videostream, not essential just QOL
def videocapture():
  # allow the camera to warmup
  sleep(0.1)

  # capture frames from the camera
  for frame in camera.capture_continuous(stream, format="bgr", use_video_port=True):
      # grab the raw NumPy array representing the image, then initialize the timestamp
      # and occupied/unoccupied text
      image = frame.array

      # show the frame
      cv2.imshow("Frame", image)
      key = cv2.waitKey(1) & 0xFF

      # clear the stream in preparation for the next frame
      stream.truncate(0)

      # if the `q` key was pressed, break from the loop
      if key == ord("q"):
	      break

def blokje():
    sleep(0.1)

    # define range of blue color in HSV
    lower_blue = np.array([100, 150, 120 ])
    upper_blue = np.array([140, 255, 255])
    while True:
        camera.capture(stream, 'bgr', use_video_port=True)

        blurred_frame = cv2.GaussianBlur(stream.array, (5, 5), 0)
        hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        contours, h = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        x = 0
        y = 0

        for contour in contours:
            rect = cv2.boundingRect(contour)

            x,y,w,h = rect
            
            
            cv2.rectangle(stream.array, (x,y), (x+w, y+h), (0, 255,0), 2)
        print("X: " + str(x) + " Y: " + str(y))
        cv2.drawContours(stream.array, contours, -1, (0, 255, 0), 3)

        cv2.imshow("PiCamera", stream.array)

        key = cv2.waitKey(1) & 0xFF

        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
                break
        # reset the stream before the next capture
        stream.seek(0)
        stream.truncate()
        
    


blokje()
cv2.destroyAllWindows()
