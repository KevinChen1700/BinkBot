from MovementController import MovementController
from Remote import Remote
from Motor import Motor
import RPi.GPIO as GPIO
from time import sleep
from AX12 import Ax12

#runs the main loop
controller = Controller.getInstance()
controller.run()

class Controller:
    __instance = None

    #controller is a singleton
    @staticmethod
    def getInstance():
        if MovementController.__instance is None:
            MovementController()
        return MovementController.__instance

    def __init__(self):
        Controller.__instance = self
        GPIO.setmode(GPIO.BCM)
        self.remote = Remote.getInstance()
        self.mvcontroller = MovementController.getInstance()

    def manualRoutine(self, actionList):
        self.mvcontroller.moveMotors(actionList[3], actionList[4])
        self.mvcontroller.moveGripper(actionList[2], actionList[1])
        self.mvcontroller.moveLeftFrontWheel(1000)
        self.mvcontroller.moveRightFrontWheel(1000)

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
            try:
                data = remote1.getSignal()
                lastString = data.split("|")
                actionList = lastString[-2].split("-")
                action = actionList[-1]

                if action == "man":
                    self.manualRoutine(actionList)

                if action == "blue":
                    self.followBarRoutine()

                if action == "singleDance":
                    self.singleDanceRoutine()

                if action == "lineDanceRoutine":
                    self.lineDanceRoutine()

                if action == "survivalRunRoutine":
                    self.survivalRunRoutine()

                if action == "eggTelligence":
                    self.eggTelligenceRoutine()

            except:
                pass

            sleep(0.001)  # The loop runs every 1ms