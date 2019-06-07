import RPi.GPIO as GPIO
from time import sleep
import pigpio


class Motor:

    def __init__(self, pinArray):
        self.pi = pigpio.pi()
        self.PWM = pinArray[0]
        self.INA = pinArray[1]
        self.INB = pinArray[2]
        GPIO.setup(self.PWM, GPIO.OUT)
        self.pi.set_mode(self.PWM, pigpio.OUTPUT)
        GPIO.setup(self.INA, GPIO.OUT)
        GPIO.setup(self.INB, GPIO.OUT)
        self.pi.set_PWM_frequency(self.PWM, 100)

    def off(self):
        self.pi.set_PWM_dutycycle(self.PWM, 0)

    def move(self, direction, speed):
        speed = speed * 2.55
        
        if (speed > 0) and (speed <= 100): # speeds between 0 and 20 are unsafe
            speed = 0
        if (direction == "right") or (direction == "r"):
            GPIO.output(self.INA, 1)
            GPIO.output(self.INB, 0)
        else:
            GPIO.output(self.INA, 0)
            GPIO.output(self.INB, 1)
        sleep(0.01)  # wait 10ms
        self.pi.set_PWM_dutycycle(self.PWM, speed)
