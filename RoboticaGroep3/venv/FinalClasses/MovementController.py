from Motor import Motor
from Servo import Servo
import AX12
from time import sleep

class MovementController:
    __instance = None
    @staticmethod
    def getInstance():  # function to get the only instance of this class since the class is a singleton
        # if there isn't an instance of this class yet, create it
        if MovementController.__instance is None:
            MovementController()
        # return this class's only instance
        return MovementController.__instance

    def __init__(self):
        if MovementController.__instance is not None:  # if the constructor of this class is called more than once
            raise Exception("This class is a singleton!")
        else:
            # puts the created instance in the "__instance" variable
            MovementController.__instance = self
            # array that holds the pins of all the motors
            pinArray = [[16, 5, 6], [20, 23, 24]]
            # creates instances of the Motor class to control the physical motors
            self.leftMotor = Motor(pinArray[0])
            self.rightMotor = Motor(pinArray[1])

            self.servos = AX12.Ax12()  # list of all servos
            # creates instances of the Servo class to control the physical servos
            self.armServo = Servo(self.servos, 3, 426, 576, 100)
            self.gripServo = Servo(self.servos, 4, 280, 574, 512)
            self.leftFrontWheel = Servo(self.servos, 1, 426, 576, 110)
            self.rightFrontWheel = Servo(self.servos, 2, 280, 574, 110)

    def moveGripper(self, x, y):  # function to move the servos in the gripper
        self.armServo.move(y)
        self.gripServo.move(x)

    def moveLeftFrontWheel(self, y):  # function to move the servo that moves the left front wheel
        self.leftFrontWheel.move(y)

    def moveRightFrontWheel(self, y):  # function to move the servo that moves the right front wheel
        self.rightFrontWheel.move(y)
    
    def moveMotors(self, x, y):
        # turns the value from the joystick (0 up to 1023) into a value between -100 and 100
        turnvariable = (x - 511.5) / 5.115  # joystick value 1023 turns into 100, joystick value 0 turns into -100
        speedvariable = (y / -5.115) + 100  # joystick value 0 turns into 100, joystick value 1023 turns into -100

        # if the joystick is aimed to the right
        if turnvariable > 10:
            # if the joystick is aimed to the right and up
            if speedvariable > 10:
                self.leftMotor.move("left", speedvariable)
                self.rightMotor.move("right", speedvariable * ((100 - turnvariable) / 100))
            # if the joystick is aimed to the right and down
            elif speedvariable < -10:
                self.leftMotor.move("right", (speedvariable * -1))
                self.rightMotor.move("left", (speedvariable * -1) * ((100 - turnvariable) / 100))
            # if the joystick is aimed solely to the right
            else:
                self.leftMotor.move("left", turnvariable)
                self.rightMotor.move("left", turnvariable)

        # if the joystick is aimed to the left
        elif turnvariable < -10:
            # if the joystick is aimed to the left and up
            if speedvariable > 10:
                self.leftMotor.move("left", speedvariable * ((100 + turnvariable) / 100))
                self.rightMotor.move("right", speedvariable)
            # if the joystick is aimed to the left and down
            elif speedvariable < -10:
                self.leftMotor.move("right", (speedvariable * -1) * ((100 + turnvariable) / 100))
                self.rightMotor.move("left", (speedvariable * -1))
            # if the joystick is aimed solely to the left
            else:
                self.leftMotor.move("right", (turnvariable * -1))
                self.rightMotor.move("right", (turnvariable * -1))

        # if the joystick is aimed neither to the left or the right
        else:
            # if the  is aimed solely up
            if speedvariable > 10:
                self.leftMotor.move("left", speedvariable)
                self.rightMotor.move("right", speedvariable)
            # if the joystick is aimed solely down
            elif speedvariable < -10:
               
                self.leftMotor.move("right", (speedvariable * -1))
                self.rightMotor.move("left", (speedvariable * -1))
            # if the joystick is not being used
            else:
                self.leftMotor.off()
                self.rightMotor.off()
