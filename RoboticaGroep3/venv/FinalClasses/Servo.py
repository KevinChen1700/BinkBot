import AX12
from time import sleep

class Servo:

    def __init__(self, servos, id, maxAngle, minAngle, speed):
        self.servos = servos
        self.id = id
        self.joyState = 511
        self.currentAngle = 500
        self.maxAngle = maxAngle
        self.minAngle = minAngle
        self.speed = speed
        

    def move(self, joyState):
        if (joyState > 800) and not (self.joyState > 800):
            self.joyState = joyState
            self.currentAngle = self.maxAngle
            self.servos.moveSpeedRW(self.id, (self.currentAngle), self.speed)
            self.servos.action()
            
        elif (joyState < 300) and not (self.joyState < 300):
            self.joyState = joyState
            self.currentAngle = self.minAngle
            self.servos.moveSpeedRW(self.id, (self.currentAngle), self.speed)
            self.servos.action()
            
        elif (joyState > 300 and joyState < 800):
            if not (self.joyState > 300 and self.joyState < 800):
                self.joyState = joyState
                self.servos.move(self.id, (self.servos.readPosition(self.id)))
                self.servos.action()


    
    def getTemp(self):
        print("Servo" + str(self.id) + "Temp: " + str(self.servos.readTemperature(self.id)) + " Degrees")



        
