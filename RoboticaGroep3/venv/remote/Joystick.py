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
            GPIO.setup(21, GPIO.OUT)
            GPIO.setup(19, GPIO.IN)
            GPIO.setup(20, GPIO.OUT)
            GPIO.setup(16, GPIO.OUT)
            GPIO.setup(26, GPIO.OUT)

    def setupSpiPins(self, clkPin, misoPin, mosiPin, csPin):
        pass

    def readChannel(self, channel):
        if (channel < 0) or (channel > 7):
            print ("Invalid ADC Channel number, must be between [0,7]")
            return -1
            # Datasheet says chip select must be pulled high between conversions
        GPIO.output(26, GPIO.HIGH)
        # Start the read with both clock and chip select low
        GPIO.output(26, GPIO.LOW)
        GPIO.output(21, GPIO.HIGH)
        # read command is:
        # start bit = 1
        # single-ended comparison = 1 (vs. pseudo-differential)
        # channel num bit 2
        # channel num bit 1
        # channel num bit 0 (LSB)
        read_command = 0x18
        read_command |= channel
        sendBits(read_command, 5)
        adcValue = recvBits(12)
        # Set chip select high to end the read
        GPIO.output(16, GPIO.HIGH)
        return adcValue

    def sendBits(self, data, numBits, clkPin, mosiPin):
        data <<= (8 - numBits)

        for bit in range(numBits):
            # Set RPi's output bit high or low depending on highest bit of data field
            if data & 0x80:
                GPIO.output(mosiPin, GPIO.HIGH)
            else:
                GPIO.output(mosiPin, GPIO.LOW)

            # Advance data to the next bit
            data <<= 1

            # Pulse the clock pin HIGH then immediately low
            GPIO.output(clkPin, GPIO.HIGH)
            GPIO.output(clkPin, GPIO.LOW)

    def recvBits(self, numBits, clkPin, misoPin):
        retVal = 0

        for bit in range(numBits):
            # Pulse clock pin
            GPIO.output(clkPin, GPIO.HIGH)
            GPIO.output(clkPin, GPIO.LOW)

            # Read 1 data bit in
            if GPIO.input(misoPin):
                retVal |= 0x1

            # Advance input to next bit
            retVal <<= 1

        # Divide by two to drop the NULL bit
        return (retVal / 2)