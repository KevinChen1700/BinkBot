from MovementController import MovementController

from Remote import Remote
from Motor import Motor
import RPi.GPIO as GPIO
from time import sleep
from AX12 import Ax12


class Controller:
    __instance = None

    #controller is a singleton
    @staticmethod
    def getInstance():
        if Controller.__instance is None:
            Controller()
        return Controller.__instance

    def __init__(self):
        Controller.__instance = self
        GPIO.setmode(GPIO.BCM)
        self.remote = Remote.getInstance()
        self.mvcontroller = MovementController.getInstance()

    def manualRoutine(self, actionList):
        print("Running manual routine.")
        self.mvcontroller.moveMotors(int(actionList[2]), int(actionList[3]))
        self.mvcontroller.moveGripper(int(actionList[1]), int(actionList[0]))
        #self.mvcontroller.moveLeftFrontWheel(1000)
        #self.mvcontroller.moveRightFrontWheel(1000)
        

    def followBarRoutine(self):
        print("This function is still WIP")

    def singleDanceRoutine(self):
        print("This function is still WIP")

    def lineDanceRoutine(self):
        print("This function is still WIP")

    def survivalRunRoutine(self):
        print("This function is still WIP")

    def eggTelligenceRoutine(self):
        print("This function is still WIP")

    #main loop
    def run(self):
        while True:
##            try:
##
##
##            except:
##                pass
            data = self.remote.getSignal()
            lastString = data.split("|")
            actionList = lastString[-2].split("-")
            action = actionList[-1]


            if action == "man":
                self.manualRoutine(actionList)

            elif action == "blue":
                self.followBarRoutine()

            elif action == "singleDance":
                self.singleDanceRoutine()

            elif action == "lineDanceRoutine":
                self.lineDanceRoutine()

            elif action == "survivalRunRoutine":
                self.survivalRunRoutine()

            elif action == "eggTelligence":
                self.eggTelligenceRoutine()

            sleep(0.001)  # The loop runs every 1ms
