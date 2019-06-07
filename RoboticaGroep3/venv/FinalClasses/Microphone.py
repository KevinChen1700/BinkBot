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
            Microphone.__instance = self
            #lage tonen channel 0
            self.swt_channel = 0

            #midden tonen channel 1
            self.vrx_channel = 1

            #hoge tonen channel 2
            self.vry_channel = 2

            #accu spanning channel 3
            self.vrb_channel = 3


            # Time delay, which tells how many seconds the value is read out
            self.delay = 0.01

            # Spi oeffnen
            self.spi = spidev.SpiDev()
            self.spi.open(0, 0)
            self.spi.max_speed_hz = 1000000

    # Function for reading the MCP3008 channel between 0 and 7
    def readChannel(self,channel):
        val = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((val[1] & 3) << 8) + val[2]
        return data

    #Function for displaying tonen
    def readValue (self):
        self.vrx_pos = self.readChannel(self.vrx_channel)
        self.vry_pos = self.readChannel(self.vry_channel)
        self.vrb_pos = self.readChannel(self.vrb_channel)

        # SW determine
        self.swt_val = self.readChannel(self.swt_channel)
        #self.datastring = ("VRx : {}  VRy : {}  SW : {} Accu : {}".format(self.vrb_pos, self.vrx_pos, self.vry_pos, self.swt_val))
        self.datastring = ("SW : {}  VRx : {}  VRy : {} Accu : {}".format(self.swt_val, self.vrx_pos, self.vry_pos, self.vrb_pos))
        print self.datastring


        # wait
        time.sleep(self.delay)

