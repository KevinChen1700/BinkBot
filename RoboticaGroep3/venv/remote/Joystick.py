import RPi.GPIO as GPIO
import spidev
import os


class Joystick:

    def __init__(self, pin1, pin2):
        self.spi = spidev.SpiDev()
        self.spi.open(pin1, pin2)
        self.spi.max_speed_hz = 1000000

    def readChannel(self, channel):
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    def getX(self):
        return self.readChannel(1)

    def getY(self):
        return self.readChannel(2)

