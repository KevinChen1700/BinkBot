from picamera.array import PiRGBArray
from picamera import PiCamera
from collections import deque
from imutils.video import VideoStream
import numpy as np
import sys
import time
import pyzbar.pyzbar as pyzbar
import cv2
import imutils
import argparse

#Function to test videostream, not essential just QOL
def videocapture():
  # allow the camera to warmup
  time.sleep(0.1)

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

def qrScanner():
  while True:
    camera.capture(stream, 'bgr', use_video_port=True)
    # stream.array now contains the image data in BGR order
    decodedObjects = pyzbar.decode(stream.array)
    if len(decodedObjects):
      zbarData = decodedObjects[0].data
    else:
      zbarData=''
    if zbarData:
      cv2.putText(stream.array, "ZBAR : {}".format(zbarData), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
      cv2.putText(stream.array, "ZBAR : QR Code NOT Detected", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    #display(stream.array, decodedObjects)
    cv2.imshow('frame', stream.array)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
    # reset the stream before the next capture
    stream.seek(0)
    stream.truncate()

def lineDetector(): #werkt maar alleen 1 frame, gaat niet steeds door
  while True:
    #Capture image
    camera.capture(stream, 'bgr', use_video_port=True)
    #img = stream.array

    #Convert to Grayscale
    gray = cv2.cvtColor(stream.array, cv2.COLOR_BGR2GRAY)

    #Blur image to reduce noise
    #blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    #blurred = cv2.medianBlur(gray,5)
    blurred = cv2.bilateralFilter(gray,9,75,75)

    #Perform canny edge-detection
    edged = cv2.Canny(blurred, 25, 50)

    #Perform hough lines probalistic transform
    lines = cv2.HoughLinesP(edged,1,np.pi/180,10,80,1)

    #Draw lines on input image
    if(lines is not None):
        for x1,y1,x2,y2 in lines[0]:
            cv2.line(stream.array,(x1,y1),(x2,y2),(0,255,0),2)

    cv2.imshow('Frame', stream.array)
    cv2.waitKey(1)
    stream.seek(0)
    stream.truncate()

def blue():
  # define range of blue color in HSV
  lower_blue = np.array([100,150,0])
  upper_blue = np.array([140,255,255])
  while True:
    camera.capture(stream, 'bgr', use_video_port=True)

    # resize the frame, blur it, and convert it to the HSV
    # color space
    blurred = cv2.GaussianBlur(stream.array, (11, 11), 0, 1)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    imgray = cv2.cvtColor(stream.array,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgray, lower_blue, upper_blue)
    contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    center = None
    if len(contours) > 0:
      cv2.drawContours(stream.array, contours, -1, (0,255,255), 2, 8)
    cv2.imshow('Frame', stream.array)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
            break
    # reset the stream before the next capture
    stream.seek(0)
    stream.truncate()

def black():
  # define range of blue color in HSV
  lower_black = np.array([0, 0, 0 ])
  upper_black = np.array([180, 255, 40])# edit 3rd higher to get lighter colors
  while True:
    camera.capture(stream, 'bgr', use_video_port=True)

    # resize the frame, blur it, and convert it to the HSV
    # color space
    blurred = cv2.GaussianBlur(stream.array, (11, 11), 0, 1)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    imgray = cv2.cvtColor(stream.array,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgray, lower_black, upper_black)
    contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    center = None
    if len(contours) > 0:
      cv2.drawContours(stream.array, contours, -1, (0,255,255), 2, 8)
    cv2.imshow('Frame', stream.array)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
            break
    # reset the stream before the next capture
    stream.seek(0)
    stream.truncate()

# Display barcode and QR code location
def display(im, decodedObjects):

  # Loop over all decoded objects
  for decodedObject in decodedObjects:
    points = decodedObject.polygon

    # If the points do not form a quad, find convex hull
    if len(points) > 4 :
      hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
      hull = list(map(tuple, np.squeeze(hull)))
    else :
      hull = points;

    # Number of points in the convex hull
    n = len(hull)

    # Draw the convex hull
    for j in range(0,n):
      cv2.line(im, hull[j], hull[ (j+1) % n], (255,0,0), 3)

  # Display results
  # cv2.imshow("Results", im);
    cv2.destroyAllWindows()

#declare camera properties, resolution is now stable, framerate may be adjusted for better performance
camera = PiCamera()
camera.resolution = (400, 400)
camera.framerate = 90
stream = PiRGBArray(camera, size=(400, 400))
#videocapture()
#qrScanner()
blue()
#black()
#lineDetector()
#groen()
#rood()
cv2.destroyAllWindows()
