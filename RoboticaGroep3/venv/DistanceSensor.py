# Libraries
import RPi.GPIO as GPIO
import time
from Sensor import Sensor


class DistanceSensor(Sensor):
    on = False
    data

    def __init__(self, trigger, echo):
        # GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)

        # set GPIO Pins
        GPIO_TRIGGER = trigger
        GPIO_ECHO = echo

        # set GPIO direction (IN / OUT)
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)

    def onOff(self):
        on = not on

    while on:
        # set Trigger to HIGH
        GPIO.output(GPIO_TRIGGER, True)

        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)

        StartTime = time.time()
        StopTime = time.time()

        # save StartTime
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()

        # save time of arrival
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()

        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        data = (TimeElapsed * 34300) / 2
        time.sleep(0.001)
    
    def getData(self):
        return data