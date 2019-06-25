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
            # self.objDetector = objectDetector.getInstance()
            self.microphone = Microphone.getInstance()

    def manualRoutine(self, actionList):
        print("Running manual routine.")
        self.mvcontroller.moveMotors(int(actionList[2]), int(actionList[3]))
        self.mvcontroller.moveGripper(int(actionList[1]), int(actionList[0]))
        # self.mvcontroller.moveLeftFrontWheel(1000)
        # self.mvcontroller.moveRightFrontWheel(1000)

    def followBarRoutine(self):
        print("This function is still WIP")
        x, y, w, h = self.objDetector.findBlueBar()
        if x == 0:
            print("beun")
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

    def survivalRunRoutine(self):
        print("This function is still WIP")

    def eggTelligenceRoutine(self):
        print("This function is still WIP, needs buttons in UI to choose color and which qr to scan")
        distance = self.DistanceSensor.calcDistance()
        color = ""
        x, y, w, h = self.objDetector.findContainer(color)
        eggCoords, qrCodeData = self.objDetector.qrScanner()
        # inital movement to get in the eggtelligence field
        if self.startMovement is False:
            self.mvcontroller.moveMotors(0, 1023)
            # straight forward for 1 second, currently a placeholder
            sleep(1)
            self.startMovement = True

        # code to look for egg after a the initial start movement, also know as MAIN LOOP where everything happens
        if self.startMovement is True:
            # chicken detection above all, so if it finds no egg and no QR it is the chicken
            if distance < 10 and self.objDetector.qrScanner[0][0] == 0 and self.objDetector.egg == 0:
                print("rotate left")
            elif self.objDetector.blackLinedetector[0] < 50:
                print("rotate right 90 degrees")
            elif self.objDetector.blackLinedetector[0] > 300:
                print("rotate left 90 degrees")
            elif self.objDetector.blackLinedetector[1] < 50:
                print("rotate 180")
            else:
                # start looking for an egg
                print("rotate the robot around its axis until it finds something")
                # if it has found an egg
                if self.ObjectDetector.egg != 0:
                    if self.objDetector.egg < 200:
                        print("drive to the left")
                        self.mvcontroller.moveMotors(0, 511)
                    elif self.objDetector.egg > 400:
                        print("drive to the right")
                        self.mvcontroller.moveMotors(1023, 511)
                    elif 200 > self.objDetector.egg > 400:
                        print("drive forward")
                        self.mvcontroller.moveMotors(511, 1023)
                    if distance < 10 and self.eggGrabbed is False:
                        print("then make it use the gripper to pick it up")
                        self.eggGrabbed = True

                # an egg has been grabbed and needs tp be dropped off
                if self.eggGrabbed is True:
                    print("look for the container by spinning")
                    print(" if nothing found drive x amount up to a blackline and repeat")
                    if self.objDetector.qrScanner[1] == self.cityString:
                        print("city drop off found")
                        # the qr is to the left, gets first value of qrScanner. This is an array with x and y coords of the QR code, we'll take the x value which is also [0]
                        if self.objDetector.qrScanner[0][0] < 200:
                            print("drive to the left")
                            self.mvcontroller.moveMotors(0, 511)
                            if distance < 10 :
                                print("drop egg")
                                self.eggGrabbed == False
                        elif self.objDetector.qrScanner[0][0] > 400:
                            print("drive to the right")
                            self.mvcontroller.moveMotors(1023, 511)
                            if distance < 10 :
                                print("drop egg")
                                self.eggGrabbed == False
                        elif 200 > self.objDetector.qrScanner[0][0] > 400:
                            print("drive forward")
                            self.mvcontroller.moveMotors(511, 1023)
                            if distance < 10 :
                                print("drop egg")
                                self.eggGrabbed == False

                sleep(0.03333333)

    # main loop
    def run(self):
        while True:
            try:
                self.remote.sendString(str(self.microphone.getBattery()))
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

            except Exception:
                pass
