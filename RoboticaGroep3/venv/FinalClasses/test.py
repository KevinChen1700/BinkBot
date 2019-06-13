from Motor import Motor
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
pinArray = [[16, 5, 6], [20, 23, 24]]
# creates instances of the Motor class to control the physical motors
leftMotor = Motor(pinArray[0])
rightMotor = Motor(pinArray[1])


try:
    while True:
        print("1")
        leftMotor.move("left" , 100)
        sleep(0.3)
        print("2")
        leftMotor.move("right",100)
        sleep(0.1)
        print("3")
        leftMotor.move("left" , 100)
        sleep(0.5)
        print("4")
        leftMotor.move("right",100)
        sleep(0.01)
        print("5")
        leftMotor.move("left" , 100)
        sleep(0.03)
        print("6")
        leftMotor.move("right",100)
        sleep(0.4)
        print("7")
        leftMotor.move("left" , 100)
        sleep(0.1)
        print("8")
        leftMotor.move("right",100)
        sleep(0.8)

except KeyboardInterrupt:
        leftMotor.off()
        GPIO.cleanup()
