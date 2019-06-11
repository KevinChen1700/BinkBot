from MovementController import MovementController
from objectDetector import objectDetector
from Remote import Remote
from Motor import Motor
import RPi.GPIO as GPIO
from time import sleep
from AX12 import Ax12
from Microphone import Microphone


class Controller:
    __instance = None

    # controller is a singleton
    @staticmethod
    def getInstance():
        if Controller.__instance is None:
            Controller()
        return Controller.__instance

    def __init__(self):
        if Controller.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Controller.__instance = self
            GPIO.setmode(GPIO.BCM)
            self.remote = Remote.getInstance()
            self.mvcontroller = MovementController.getInstance()
            self.objDetector = objectDetector.getInstance()
            self.microphone = Microphone.getInstance()

    def manualRoutine(self, actionList):
        print("Running manual routine.")
        self.mvcontroller.moveMotors(int(actionList[2]), int(actionList[3]))
        self.mvcontroller.moveGripper(int(actionList[1]), int(actionList[0]))
        # self.mvcontroller.moveLeftFrontWheel(1000)
        # self.mvcontroller.moveRightFrontWheel(1000)

    def followBarRoutine(self):
        print("This function is still WIP")
        x, y, w, h = objDetector.findBlueBar()

        if x < 310:
            self.mvcontroller.moveMotors(0, 511)

        elif x > 330:
            self.mvcontroller.moveMotors(1023, 511)


    def singleDanceRoutine(self):
        print("This function is still WIP")

    def lineDanceRoutine(self):
        low = self.microphone.getLowTone()
        mid = self.microphone.getMidTone()
        high = self.microphone.getHighTone()

        if low > 50:
            print "low tone dance"
            #arm eerst boven, dan gripper open, sluiten, arm weer naar beneden
            self.mvcontroller.moveGripper(1023, 511)
            time.sleep(1)
            self.mvcontroller.moveGripper(1023, 1023)
            time.sleep(1)
            self.mvcontroller.moveGripper(1023, 511)
            time.sleep(1)
            self.mvcontroller.moveGripper(0, 511)
            time.sleep(1)
            self.mvcontroller.moveGripper(0, 1023)
            time.sleep(1)
            self.mvcontroller.moveGripper(0, 511)
            time.sleep(1)
            self.mvcontroller.moveGripper(511, 511)

        if mid and low > 50:
            print "doing average robot dance"
            self.mvcontroller.moveMotors(1023, 511)


        if high and mid and low > 50:
            print "doing fast robot dance"
            #op en neer bewegen van armen, dan een paar rondjes draaien?
            self.mvcontroller.moveGripper(800, 511)
            time.sleep(0.1)
            self.mvcontroller.moveGripper(300, 511)
            time.sleep(0.1)
            self.mvcontroller.moveGripper(800, 511)
            time.sleep(0.1)
            self.mvcontroller.moveGripper(300, 511)
            time.sleep(0.1)
            self.mvcontroller.moveGripper(800, 511)
            time.sleep(0.1)
            self.mvcontroller.moveGripper(300, 511)
            time.sleep(0.1)

    def survivalRunRoutine(self):
        print("This function is still WIP")

    def eggTelligenceRoutine(self):
        print("This function is still WIP")

    # main loop
    def run(self):
        while True:
            try:
                data = self.remote.getSignal()
                self.remote.sendString(str(self.microphone.getBattery()))
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

            except Exception:
                print Exception + (" WOEEPSIEEEFLOEEEEPSIEEE")
                pass
