import RPi.GPIO as GPIO
from time import sleep
import pigpio


class Motor:

    def __init__(self, pinArray):
        # sets the pins for this motor
        self.pi = pigpio.pi()
        self.PWM = pinArray[0]
        self.INA = pinArray[1]
        self.INB = pinArray[2]
        GPIO.setup(self.PWM, GPIO.OUT)
        self.pi.set_mode(self.PWM, pigpio.OUTPUT)
        GPIO.setup(self.INA, GPIO.OUT)
        GPIO.setup(self.INB, GPIO.OUT)
        self.pi.set_PWM_frequency(self.PWM, 100)
        # variables to track speed and direction
        self.speed = 80
        self.direction = "None"

    def off(self):
        self.pi.set_PWM_dutycycle(self.PWM, 0)

    def move(self, direction, speed):
        # speed is a number between 0 and 255, but the speed used in set_PWM_dutycycle is a number between 0 and 255
        speed = speed * 2.55

        if self.direction != direction:  # if the desired direction is different than the current direction
            self.direction = direction  # sets direction to desired direction
            self.speed = 80  # sets speed to minimum so the motor can warm up
            self.pi.set_PWM_dutycycle(self.PWM, 0)  # temporarily turns off the motor
            sleep(0.01)  # wait 10ms
            # switches to the desired direction
            if direction == "right":
                GPIO.output(self.INA, 1)
                GPIO.output(self.INB, 0)
            elif direction == "left":
                GPIO.output(self.INA, 0)
                GPIO.output(self.INB, 1)
            sleep(0.01)  # wait 10ms

        if self.speed < speed:  # slowly accelerates to the desired speed
            self.speed = self.speed + (speed * 0.01)
            if self.speed > 255:
                self.speed = 255

        if not (self.speed <= 80):  # speeds between 0 and 80 are unsafe
            self.pi.set_PWM_dutycycle(self.PWM, self.speed)
