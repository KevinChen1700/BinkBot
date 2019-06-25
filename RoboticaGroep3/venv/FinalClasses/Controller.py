from MovementController import MovementController
from ObjectDetector import ObjectDetector
from Remote import Remote
from Motor import Motor
import RPi.GPIO as GPIO
from time import sleep
from AX12 import Ax12
from Microphone import Microphone
from LedStrip import LedStrip
from neopixel import *
import threading


class Controller:
    __instance = None
    @staticmethod
    def getInstance():  # function to get the only instance of this class since the class is a singleton
        # if there isn't an instance of this class yet, create it
        if Controller.__instance is None:
            Controller()
        # return this class's only instance
        return Controller.__instance

    def __init__(self):
        if Controller.__instance != None:  # if the constructor of this class is called more than once
            raise Exception("This class is a singleton!")
        else:
            # puts the created instance in the "__instance" variable
            Controller.__instance = self
            self.cameraBool = True
            self.ledBool = True
            self.previousRoutine = " "
            self.actionList = [511, 511, 511, 511, "man"]
            self.motorState = [511, 511]
            GPIO.setmode(GPIO.BCM)
            self.remote = Remote.getInstance()
            self.mvcontroller = MovementController.getInstance()
            self.microphone = Microphone.getInstance()
            self.beatCount = 0
            self.prevLow = 0
            self.forward = False
            try:  # try catch so the program can still run if the camera is not plugged in
                self.objDetector = ObjectDetector.getInstance()
            except Exception:
                self.cameraBool = False
                pass
            try:  # try catch so the program can still run if the camera is not plugged in
                self.ledStrip = LedStrip(16, 19)
            except Exception:
                self.ledBool = False
                pass

            self.prevLowToneValue = 0

    def manualRoutine(self, actionList):
        print("Running manual routine.")
        self.motorState = [int(actionList[2]), int(actionList[3])]
        self.mvcontroller.moveGripper(int(actionList[1]), int(actionList[0]))
        sleep(0.001)

    def followBarRoutine(self):
        print("This function is still WIP")
        x, y, w, h = self.objDetector.findBlueBar()
        if x == 0:
            self.mvcontroller.moveMotors(511, 511)
            print("nu niet bewegen!")
        elif x < 300:
            self.mvcontroller.moveMotors(0, 511)

        elif x > 400:
            self.mvcontroller.moveMotors(1023, 511)
            # 1023=naar rechts
        else:
            self.mvcontroller.moveMotors(511, 511)
            print("nu niet bewegen!")

        sleep(0.00)

    def moveSwitch(self):
        if self.forward:
            print("moveswitchfor")
            self.forward = not self.foward
            self.mvcontroller.moveGripper(0, 511)
            self.motorState = [511, 1023]
            if self.ledBool:
                self.ledStrip.setColor(Color(0, 255, 0))

        else:
            print("moveswitchback")
            self.forward = not self.foward
            self.mvcontroller.moveGripper(1023, 511)
            self.motorState = [511, 0]
            if self.ledBool:
                self.ledStrip.setColor(Color(0, 0, 0))


    def singleDanceRoutine(self):
        print("singleDance function is still WIP")
        low = self.microphone.getLowTone()
        if (low - self.prevLow) > 50:
            print("ja")
            self.beatCount += 1
            if self.beatCount % 2 == 0:
                print("moveswitch")
                moveSwitch()
        self.prevLow = low

    def lineDanceRoutine(self):
        print("lineDance function is still WIP")
        low = self.microphone.getLowTone()
        #mid = self.microphone.getMidTone()
        #high = self.microphone.getHighTone()

        # nog min en max angle en de speed van de servos aanpassen als de robot aan het dansen is
        # if (temp - 60) > self.prevLowToneValue:
        if low > 60:
            print("test")
            self.mvcontroller.moveGripper(0, 511)
            if self.ledBool:
                self.ledStrip.setColor(Color(0, 255, 0))
            sleep(0.25)

        #elif high > 60:
        #    self.ledStrip.setColor(Color(233, 255, 0))

        #elif mid > 60:
        #   self.ledStrip.setColor(Color(255, 0, 0))

        else:
            if self.ledBool:
                self.ledStrip.setColor(Color(0, 0, 0))
            self.mvcontroller.moveGripper(1023, 511)

        #if low < 60:
        #    self.mvcontroller.moveGripper(1023, 511)

    def survivalRunRoutine(self):
        print("This function is still WIP")

    def eggTelligenceRoutine(self):
        print("This function is still WIP, needs buttons in UI to choose color and which qr to scan")
        color = ""
        x, y, w, h = self.objDetector.findContainer(color)
        qrCode = self.objDetector.qrScanner()

        sleep(0.03333333)

    def resetState(self):
        sleep(0.1)
        self.mvcontroller.moveGripper(1023, 1023)
        self.mvcontroller.moveMotors(511, 511)
        if self.ledBool:
            self.ledStrip.setColor(Color(0, 0, 255))
        # danceroutines uit als die aanstonden
        sleep(2)

    def updateActionList(self):
        while True:
            self.remote.sendString(str(self.microphone.getBattery()))
            data = self.remote.getSignal()
            lastString = data.split("|")
            self.actionList = lastString[-2].split("-")

    def motorLoop(self):
        while True:
            self.mvcontroller.moveMotors(self.motorState[0], self.motorState[1])

    # main loop
    def run(self):
        connectionThread = threading.Thread(target=self.updateActionList, args=())
        connectionThread.start()
        motorThread = threading.Thread(target=self.motorLoop, args=())
        motorThread.start()

        while True:
            try:
                action = self.actionList[-1]

                if self.previousRoutine != action:
                    self.previousRoutine = action
                    self.resetState()
                    # zet danceroutine aan als action single dance is

                if action == "man":
                    self.manualRoutine(self.actionList)

                elif action == "blue" and self.cameraBool:
                    self.followBarRoutine()

                elif action == "singleDance" and self.cameraBool:
                    self.singleDanceRoutine()

                elif action == "lineDance":
                    self.lineDanceRoutine()

                elif action == "survivalRun":
                    self.survivalRunRoutine()

                elif action == "eggTelligence" and self.cameraBool:
                    self.eggTelligenceRoutine()

            except Exception:
                pass
