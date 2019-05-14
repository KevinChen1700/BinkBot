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
        self.pi.set_mode(PWM, pigpio.OUTPUT)
        GPIO.setup(INA, GPIO.OUT)
        GPIO.setup(INB, GPIO.OUT)
        self.pi.set_PWM_frequency(self.PWM, 100)

    def off(self):
            self.pi.set_PWM_dutycycle(self.PWM, 0)

    def move(self, right, left, speed):
        GPIO.output(self.INA, right)  # ina op 1 instellen inb op 0, zodat motor naar rechts draait
        GPIO.output(self.INB, left)
        sleep(0.01)  # wait 10ms
        self.pi.set_PWM_dutycycle(self.PWM, speed)  # nieuwe snelheid als pwm instellen
