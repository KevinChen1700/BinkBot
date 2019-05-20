import RPi.GPIO as GPIO
import time
import sys


class Joystick:
    __instance = None
    @staticmethod
    def getInstance():
        if Joystick.__instance == None:
            Joystick()
        return Joystick.__instance

    def __init__(self):
        if Joystick.__instance != None:
            print("Singleton class already has an instance")
        else:
            Joystick.__instance = self
            GPIO.setmode(GPIO.BCM)
            setupSpiPins(21, 19, 20, 16)

    def setupSpiPins(clkPin, misoPin, mosiPin, csPin):
        pass

    def readChannel(channel):
        if (channel < 0) or (channel > 7):
            print "Invalid ADC Channel number, must be between [0,7]"
            return -1

        read_command = 0x18
        read_command |= channel

        sendBits(read_command, 5, 18, 23)

        adcValue = recvBits(12, 18, 24)

        return adcValue

    def sendBits(data, numBits, clkPin, mosiPin):
        data <<= (8 - numBits)
        for bit in range(numBits):
            pass

    def recvBits(numBits, clkPin, misoPin):
        retVal = 0
        return (retVal / 2)