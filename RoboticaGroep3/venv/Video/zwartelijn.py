import numpy as np
import cv2

cap = cv2.VideoCapture(0)

#frame = cv2.imread("vloer2.jpg")








while True:
    index = 0
    rect = 0, 0, 0, 0

    ret, frame = cap.read()
    # Height and width of image
    height = 480
    width = 640
    # Y , X
    roi = frame[height / 2:height, 0:width]


    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = 255 - gray
    ret, thresh = cv2.threshold(gray, 250, 255, cv2.THRESH_TOZERO)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #frame = cv2.drawContours(frame, contours, -1, (0, 0, 255), 3)

    for contour in contours:
        print(cv2.contourArea(contours[index]))
        area = cv2.contourArea(contours[index])
        if  area > 200 and area < 6000:
            rect = cv2.boundingRect(contour)
            # Deze code kan weg na testen
            x, y, w, h = rect
            cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.drawContours(roi, contours[index], -1, (0, 255, 0), 3)
            print(area)

    index = index + 1
    cv2.imshow("Region of interest", roi)
    cv2.imshow("Frame", frame)
    cv2.imshow("Gray", gray)


    if cv2.waitKey(1) == 27:
        break
cap.release()
cv2.destroyAllWindows()

