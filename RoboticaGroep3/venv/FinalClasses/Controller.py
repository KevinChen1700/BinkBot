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
            self.previousRoutine = " "
            GPIO.setmode(GPIO.BCM)
            self.remote = Remote.getInstance()
            self.mvcontroller = MovementController.getInstance()
            try:  # try catch so the program can still run if the camera is not plugged in
                self.objDetector = ObjectDetector.getInstance()
            except Exception:
                self.cameraBool = False
                pass

            self.microphone = Microphone.getInstance()
            self.ledStrip = LedStrip(16, 13)
            self.prevLowToneValue = 0

    def manualRoutine(self, actionList):
        print("Running manual routine.")
        self.mvcontroller.moveMotors(int(actionList[2]), int(actionList[3]))
        self.mvcontroller.moveGripper(int(actionList[1]), int(actionList[0]))
        self.mvcontroller.moveLeftFrontWheel(1000)
        self.mvcontroller.moveRightFrontWheel(1000)
        sleep(0.001)

    def followBarRoutine(self):
        print("This function is still WIP")
        x, y, w, h = self.objDetector.findBlueBar()
        if x == 0:
            self.mvcontroller.moveMotors(511, 511)
        elif x < 310:
            self.mvcontroller.moveMotors(0, 511)

        elif x > 330:
            self.mvcontroller.moveMotors(1023, 511)

        sleep(0.03333333)
        


    def singleDanceRoutine(self):
        print("This function is still WIP")

    def lineDanceRoutine(self):
        print("This function is still WIP")
        temp = self.microphone.getLowTone()

        # nog min en max angle en de speed van de servos aanpassen als de robot aan het dansen is
        # if (temp - 60) > self.prevLowToneValue:
        if (temp - 60) > 0:
            print("test")
            self.mvcontroller.moveGripper(0, 511)
            self.ledStrip.setColor(Color(233, 255, 0))
            sleep(0.25)
        else:
            self.mvcontroller.moveGripper(1023, 511)
            self.ledStrip.setColor(Color(0, 0, 0))
        self.prevLowToneValue = temp

    def survivalRunRoutine(self):
        print("This function is still WIP")

    def eggTelligenceRoutine(self):
        print("This function is still WIP")

    def resetState(self):
        sleep(0.1)
        self.mvcontroller.moveGripper(1023, 1023)
        self.mvcontroller.moveMotors(511, 511)
        self.mvController.moveLeftFrontWheel(1023)
        self.mvController.moveRightFrontWheel(1023)
        self.ledStrip.setColor(Color(0, 0, 0))
        sleep(2)

    # main loop
    def run(self):
        while True:
            try:
                # test of dit perse uit moet tijdens dans en autonoom of dat de delay klein genoeg is als er geen sleeps zitten in de remote
                self.remote.sendString(str(self.microphone.getBattery()))
                data = self.remote.getSignal()
                lastString = data.split("|")
                actionList = lastString[-2].split("-")
                action = actionList[-1]
                if self.previousRoutine != action:
                    self.previousRoutine = action
                    self.resetState()
                if action == "man":
                    self.manualRoutine(actionList)

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
