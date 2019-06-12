import spidev
import os


class Microphone:
    __instance = None
    @staticmethod
    def getInstance():  # function to get the only instance of this class since the class is a singleton
        # if there isn't an instance of this class yet, create it
        if Microphone.__instance is None:
            Microphone()
        # return this class's only instance
        return Microphone.__instance

    def __init__(self):
        if Microphone.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            # puts the created instance in the "__instance" variable
            Microphone.__instance = self
            # open spi
            self.spi = spidev.SpiDev()
            self.spi.open(0, 0)
            self.spi.max_speed_hz = 1000000

    # function for reading the MCP3008 channel between 0 and 7
    def readChannel(self, channel):
        val = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((val[1] & 3) << 8) + val[2]
        return data

    # functions to read specific channels associated with specific tones or the battery voltage
    def getLowTone(self):
        return self.readChannel(0)

    def getMidTone(self):
        return self.readChannel(1)

    def getHighTone(self):
        return self.readChannel(2)

    def getBattery(self):
        return self.readChannel(3)


