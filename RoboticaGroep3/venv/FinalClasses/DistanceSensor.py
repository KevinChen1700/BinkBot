import RPi.GPIO as GPIO
import time


class DistanceSensor:

    # sets the parameters as gpio pins
    def __init__(self, trigger, echo):
        self.trigger = trigger
        self.echo = echo
        GPIO.setup(trigger, GPIO.OUT)
        GPIO.setup(echo, GPIO.IN)
        GPIO.output(trigger, GPIO.LOW)

    # calculates distance by multiplying time by speed of sound
    def calcDistance(self):
        GPIO.output(self.trigger, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.trigger, GPIO.LOW)
        while GPIO.input(self.echo) == 0:
            pulse_start_time = time.time()
        while GPIO.input(self.echo) == 1:
            pulse_end_time = time.time()
        pulse_duration = pulse_end_time - pulse_start_time
        return round(pulse_duration * 17150, 2)

