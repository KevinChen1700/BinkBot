from MovementController import MovementController

from Motor import Motor
from Remote import Remote
import RPi.GPIO as GPIO

from time import sleep

from AX12 import Ax12

GPIO.setmode(GPIO.BCM)


test = Ax12()

mvcontroller = MovementController()
while True:
    sleep(3.4)
    mvcontroller.moveGripper(1000, 1000)
    sleep(3.4)
    mvcontroller.moveGripper(1000, 0)
    sleep(3.41)

    mvcontroller.moveMotors(511,511)



