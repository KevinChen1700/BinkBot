from Microphone import Microphone
from MovementController import MovementController
from ObjectDetector import ObjectDetector


class DanceRoutines:

    def __init__(self, ledstrip):
        self.microphone = Microphone.getInstance()
        self.mvcontroller = MovementController.getInstance()
        self.objdetector = ObjectDetector.getInstance()
        self.ledStrip = ledstrip
        self.beatCount = 0
        self.prevLow = 0
        self.forward = False
        self.ledBool = True
        self.motorState = [511, 511]
        try:
            self.ledStrip.setColor(Color(0, 0, 0))
        except Exception:
            self.ledBool = False
            pass


    def runSingleDance(self):
        if self.objdetector.blackLineDetector():
            self.motorState = [511, 0]
        self.mvcontroller.moveMotors(self.motorState[0], self.motorState[1])
        low = self.microphone.getLowTone()
        if (low - self.prevLow) > 50:
            self.beatCount += 1
            if self.beatCount % 2 == 0:
                moveSwitch()

    def moveSwitch(self):
        if self.forward:
            self.forward = not self.foward
            self.mvcontroller.moveGripper(0, 511)
            self.motorState = [511, 1023]
            if self.ledBool:
                self.ledStrip.setColor(Color(0, 255, 0))

        else:
            self.forward = not self.foward
            self.mvcontroller.moveGripper(1023, 511)
            self.motorState = [511, 0]
            if self.ledBool:
                self.ledStrip.setColor(Color(0, 0, 0))



