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
        self.minSpeed = 80
        self.speed = self.minSpeed
        self.direction = "None"

    def off(self):
        self.move(self.direction, 0)

    def move(self, direction, speed):
        #speed has to be a number between 0 and 100
        if speed > 100:
            speed = 100
        if speed < 0:
            speed = 0
        # speed is a number between 0 and 100, but the speed used in set_PWM_dutycycle is a number between 0 and 255
        speed = speed * 2.55

        if self.direction != direction:  # if the desired direction is different than the current direction
            delay = (self.speed / 1500) + 0.05  # calculates a delay based on the speed of the motor
            self.direction = direction  # sets direction to desired direction
            self.speed = self.minSpeed  # sets speed to minimum so the motor can warm up
            self.pi.set_PWM_dutycycle(self.PWM, 0)  # temporarily turns off the motor
            sleep(delay)  # wait the delay calculated above
            # switches to the desired direction
            if direction == "right":
                GPIO.output(self.INA, 1)
                GPIO.output(self.INB, 0)
            elif direction == "left":
                GPIO.output(self.INA, 0)
                GPIO.output(self.INB, 1)
            sleep(delay)  # wait the delay calculated above

        if self.speed < speed:  # slowly accelerates to the desired speed
            self.speed = self.speed + (speed * (0.00007 * self.speed))  #accelerates faster as speed increases
            if self.speed > 255:
                self.speed = 255
        else:  # slowly decelerates to the desired speed
            self.speed = self.speed - ((255 - speed) * 0.04)  #decelerates based on how low speed is
            if self.speed < 80:
                self.speed = 80

        if not (self.speed <= self.minSpeed):  # speeds between 0 and 80 are unsafe
            self.pi.set_PWM_dutycycle(self.PWM, self.speed)
        else:
            self.pi.set_PWM_dutycycle(self.PWM, 0)
