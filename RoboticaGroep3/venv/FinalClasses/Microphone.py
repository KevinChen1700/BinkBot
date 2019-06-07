import spidev
import os
import time


class Microphone:
    __instance = None

    @staticmethod
    def getInstance():
        if Microphone.__instance is None:
            Microphone()
        return Microphone.__instance

    def __init__(self):
        if Microphone.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Microphone.__instance = self

            # channel for low tones
            self.swt_channel = 0

            # channel for mid tones
            self.vrx_channel = 1

            # channel for high tones
            self.vry_channel = 2

            # output battery voltage
            self.vrb_channel = 3

            # open spi
            self.spi = spidev.SpiDev()
            self.spi.open(0, 0)
            self.spi.max_speed_hz = 1000000

    # Function for reading the MCP3008 channel between 0 and 7
    def readChannel(self, channel):
        val = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((val[1] & 3) << 8) + val[2]
        return data

    # Shows which tone is being read
    def getLowTone(self):
        self.swt_val = self.readChannel(self.swt_channel)
        return self.swt_val

    def getMidTone(self):
        self.vrx_pos = self.readChannel(self.vrx_channel)
        return self.vrx_pos

    def getHighTone(self):
        self.vry_pos = self.readChannel(self.vry_channel)
        return vry_pos


