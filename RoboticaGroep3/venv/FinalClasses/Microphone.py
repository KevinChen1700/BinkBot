import spidev
import os
import time

class Microphone:
    __instance = None
    @staticmethod
    def getInstance():
         if Microphone.__instance == None:
             Microphone()
         return Microphone.__instance


    def __init__(self):
        if Microphone.__instance != None:
            raise Exception("This class is a singleton!")
        else:

            #self.swt_channel = swt_channel
            #self.vrx_channel = vrx_channel
            #self.vry_channel = vry_channel
            #self.vrb_channel = vrb_channel

            self.swt_channel = 0
            self.vrx_channel = 1
            self.vry_channel = 2
            self.vrb_channel = 3


            # Time delay, which tells how many seconds the value is read out
            self.delay = 0.5

            # Spi oeffnen
            spi = spidev.SpiDev()
            spi.open(0, 0)
            spi.max_speed_hz = 1000000

    # Function for reading the MCP3008 channel between 0 and 7
    def readChannel(self,channel):
        self.val = spi.xfer2([1, (8 + self.channel) << 4, 0])
        data = ((self.val[1] & 3) << 8) + self.val[2]
        return data

    #Function for displaying tonen
    def readValue (self):
        self.vrx_pos = readChannel(self.vrx_channel)
        self.vry_pos = readChannel(self.vry_channel)
        self.vrb_pos = readChannel(self.vrb_channel)

        # SW determine
        self.swt_val = readChannel(self.swt_channel)
        datastring = ("VRx : {}  VRy : {}  SW : {} Accu : {}".format(self.vrb_pos, self.vrx_pos, self.vry_pos, self.swt_val))
        print datastring


        # wait
        time.sleep(self.delay)

    # endless loop to test
    while True:
        readValue()





