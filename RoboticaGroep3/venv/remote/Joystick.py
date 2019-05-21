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
            self.CLK = 21
            self.MISO = 19
            self.MOSI = 20
            self.CS = 16
            GPIO.setup(self.CLK, GPIO.OUT)
            GPIO.setup(self.MISO, GPIO.IN)
            GPIO.setup(self.MOSI, GPIO.OUT)
            GPIO.setup(self.CS, GPIO.OUT)

    def readChannel(self, channel):
        if (channel < 0) or (channel > 7):
            print ("Invalid ADC Channel number, must be between [0,7]")
            return -1
            # Datasheet says chip select must be pulled high between conversions
        GPIO.output(self.CS, GPIO.HIGH)
        # Start the read with both clock and chip select low
        GPIO.output(self.CS, GPIO.LOW)
        GPIO.output(self.CLK, GPIO.LOW)
        # read command is:
        # start bit = 1
        # single-ended comparison = 1 (vs. pseudo-differential)
        # channel num bit 2
        # channel num bit 1
        # channel num bit 0 (LSB)
        read_command = 0x18
        read_command |= channel
        self.sendBits(read_command, 5)
        adcValue = self.recvBits(12)
        # Set chip select high to end the read
        GPIO.output(self.CS, GPIO.HIGH)
        return adcValue / 2

    def sendBits(self, data, numBits):
        data <<= (8 - numBits)

        for bit in range(numBits):
            # Set RPi's output bit high or low depending on highest bit of data field
            if data & 0x80:
                GPIO.output(self.MOSI, GPIO.HIGH)
            else:
                GPIO.output(self.MOSI, GPIO.LOW)

            # Advance data to the next bit
            data <<= 1

            # Pulse the clock pin HIGH then immediately low
            GPIO.output(self.CLK, GPIO.HIGH)
            GPIO.output(self.CLK, GPIO.LOW)

    def recvBits(self, numBits):
        retVal = 0

        for bit in range(numBits):
            # Pulse clock pin
            GPIO.output(self.CLK, GPIO.HIGH)
            GPIO.output(self.CLK, GPIO.LOW)

            # Read 1 data bit in
            if GPIO.input(self.MISO):
                retVal |= 0x1

            # Advance input to next bit
            retVal <<= 1

        # Divide by two to drop the NULL bit
        return (retVal / 2)
