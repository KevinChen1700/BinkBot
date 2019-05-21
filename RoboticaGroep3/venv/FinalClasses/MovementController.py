from Motor import Motor
import AX12

class MovementController:
    __instance = None
    @staticmethod
    def getInstance():
        if MovementController.__instance == None:
            MovementController()
        return MovementController.__instance

    def __init__(self):
        if MovementController.__instance != None:
            raise Exception("This class is a singelton!")
        else:
            pinArray = [[16,5,6],[20,23,24]]

            print(pinArray[0])
            print(pinArray[1])

            self.leftMotor = Motor(pinArray[0])
            self.rightMotor = Motor(pinArray[1])

            self.servos = AX12.Ax12()
            self.servospeed = 200


    def move(self, x, y):
        # turns the value from the joystick (0 up to 1023) into a value between -100 and 100
        speedvariabele = (y / -5.115) + 100  # joystick value 0 turns into 100, joystick value 1023 turns into -100
        turnvariabele = (x - 511.5) / 5.115  # joystick value 1023 turns into 100, joystick value 0 turns into -100

        # if the joystick is aimed to the right
        if turnvariabele > 10:
            # if the joystick is aimed to the right and up
            if speedvariabele > 10:
                self.leftMotor.move("left", speedvariabele)
                self.rightMotor.move("right", speedvariabele * ((100 - turnvariabele) / 100))
            # if the joystick is aimed to the right and down
            elif speedvariabele < -10:
                self.leftMotor.move("right", (speedvariabele * -1))
                self.rightMotor.move("left", (speedvariabele * -1) * ((100 - turnvariabele) / 100))
            # if the joystick is aimed solely to the right
            else:
                self.leftMotor.move("left", turnvariabele)
                self.rightMotor.move("left", turnvariabele)

        # if the joystick is aimed to the left
        elif turnvariabele < -10:
            # if the joystick is aimed to the left and up
            if speedvariabele > 10:
                self.leftMotor.move("left", speedvariabele * ((100 + turnvariabele) / 100))
                self.rightMotor.move("right", speedvariabele)
            # if the joystick is aimed to the left and down
            elif speedvariabele < -10:
                self.leftMotor.move("right", (speedvariabele * -1) * ((100 + turnvariabele) / 100))
                self.rightMotor.move("left", (speedvariabele * -1))
            # if the joystick is aimed solely to the left
            else:
                self.leftMotor.move("right", (turnvariabele * -1))
                self.rightMotor.move("right", (turnvariabele * -1))

        # if the joystick is aimed neither to the left or the right
        else:
            # if the joystick is aimed solely up
            if speedvariabele > 10:
                self.leftMotor.move("left", speedvariabele)
                self.rightMotor.move("right", speedvariabele)
            # if the joystick is aimed solely down
            elif speedvariabele < -10:
                self.leftMotor.move("right", (speedvariabele * -1))
                self.rightMotor.move("left", (speedvariabele * -1))
            # if the joystick is not being used
            else:
                self.leftMotor.off()
                self.rightMotor.off()


    def mapdeg(self,x):
        return (int)((x - 30) * (1023 - 0) / (330 - 30));

    def moveFront(self, id, angle):
        self.servos.moveSpeedRW(id, self.mapdeg(angle), self.servospeed)
        #testen wat dit doet
        self.servos.action()

    def getTemp(self, id):
        for x in id:
            print("Servo" + str(x) + "Temp: " + str(self.servos.readTemperature(x)) + "°C")