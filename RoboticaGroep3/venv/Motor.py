# import RPi.GPIO as GPIO
from time import sleep


class Motor:

    def __init__(self, PWM, INA, INB):
        self.PWM = PWM
        self.INA = INA
        self.INB = INB
        GPIO.setup(PWM, GPIO.OUT)
        GPIO.setup(INA, GPIO.OUT)
        GPIO.setup(INB, GPIO.OUT)
        VM = GPIO.PWM(PWM, 100)
        on = false

    def onOff(self):
        if self.on:
            self.VM.stop()
        else:
            self.VM.start(0)
        on = not on

    def move(self, right, left, speed):
        GPIO.output(self.INA, right)  # ina op 1 instellen inb op 0, zodat motor naar rechts draait
        GPIO.output(self.INB, left)
        sleep(0.01)  # wait 10ms
        VM1.ChangeDutyCycle(speed)  # nieuwe snelheid als pwm instellen
