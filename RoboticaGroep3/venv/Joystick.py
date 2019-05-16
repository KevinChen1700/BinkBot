from Tkinter import *
import RPi.GPIO as GPIO
import socket
import spidev
import time
import os


class Joystick:

    def __init__(self, pin1, pin2):
        # joystick code
        self.spi = spidev.SpiDev()
        self.spi.open(pin1, pin2)
        self.spi.max_speed_hz = 1000000

    def readChannel(channel):
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    # endless loop
    while True:
        # Determine position
        self.x_pos = readChannel(1)
        self.y_pos = readChannel(2)


