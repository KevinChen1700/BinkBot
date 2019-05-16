from Motor import Motor


class WheelController:

    def __init__(self, pinArray):
        self.leftMotor = Motor(pinArray[0])
        self.rightMotor = Motor(pinArray[1])


    def move(self, x, y):
        




