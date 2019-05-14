import RPi.GPIO as GPIO
from time import sleep
import pigpio


class Motor:

    def __init__(self, PWM, INA, INB):
        self.pi = pigpio.pi()
        self.PWM = PWM
        self.INA = INA
        self.INB = INB
        GPIO.setup(PWM, GPIO.OUT)
        pi.set_mode(PWM, pigpio.OUTPUT)
        GPIO.setup(INA, GPIO.OUT)
        GPIO.setup(INB, GPIO.OUT)
        self.on = false

    def onOff(self):
        if self.on:
            pi.set_PWM_frequency(PWM, 100)
        else:
            pi.set_PWM_frequency(PWM, 0)
        self.on = not on

    def move(self, right, left, speed):
        GPIO.output(self.INA, right)  # ina op 1 instellen inb op 0, zodat motor naar rechts draait
        GPIO.output(self.INB, left)
        sleep(0.01)  # wait 10ms
        self.pi.set_PWM_dutycycle(PWM, speed)  # nieuwe snelheid als pwm instellen
