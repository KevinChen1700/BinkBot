from MovementController import MovementController
from Remote import Remote
from Motor import Motor
import RPi.GPIO as GPIO
from time import sleep

from AX12 import Ax12

GPIO.setmode(GPIO.BCM)

remote1 = Remote.getInstance()
test = Ax12()
mvcontroller= MovementController.getInstance()

while True:
    try:
        test = remote1.getSignal()
        #print(test)
        data1 = test.split("|")
        #print(data1[-2])
        
        data = data1[-2].split("-")
        print(data)
        #sleep(0.4)
        #sleep(0.4)
        mvcontroller.moveGripper(int(data[2]), int(data[3]))
        #sleep(0.4)
        mvcontroller.moveGripper(int(data[2]), int(data[3]))
        #sleep(0.4)
        mvcontroller.moveMotors(int(data[0]), int(data[1]))
        #sleep(0.1)
        
        
        

    except:
        pass

