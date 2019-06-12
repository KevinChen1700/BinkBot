import AX12
from time import sleep


class Servo:

    def __init__(self, servos, id, maxAngle, minAngle, speed):
        # an instance of the servo class controls a specific id within the servo list (servos)
        self.servos = servos  # list of all servos
        self.id = id  # the id of the servo this object is controlling
        self.joyState = 511  # variable that holds the previous joyState used to see if the joystick changed position
        self.currentAngle = 500  # angle this servo is moving to or has moved to
        self.maxAngle = maxAngle  # maximum angle
        self.minAngle = minAngle  # minimum angle
        self.speed = speed  # speed the servo turns at

    # function to move the servo if the joystick is either fully up or fully down and wasn't previously in this state
    # freezes the servo in place if the joystick isn't either fully up or down
    def move(self, joyState):
        # if joystick is aimed up and wasn't previously aimed up
        if (joyState > 800) and not (self.joyState > 800):
            self.joyState = joyState
            self.currentAngle = self.maxAngle
            self.servos.moveSpeedRW(self.id, self.currentAngle, self.speed)
            self.servos.action()

        # if joystick is aimed down and wasn't previously aimed down
        elif (joyState < 300) and not (self.joyState < 300):
            self.joyState = joyState
            self.currentAngle = self.minAngle
            self.servos.moveSpeedRW(self.id, self.currentAngle, self.speed)
            self.servos.action()
            
        elif 300 <= joyState <= 800:  # if joystick is not being used
            if not 300 <= self.joyState <= 800:  # and this code hasn't been run yet
                self.joyState = joyState
                self.servos.move(self.id, (self.servos.readPosition(self.id)))
                self.servos.action()

    # returns the temperature of this servo
    def getTemp(self):
        print("Servo" + str(self.id) + "Temp: " + str(self.servos.readTemperature(self.id)) + " Degrees")
