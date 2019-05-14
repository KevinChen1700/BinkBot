import RPi.GPIO as GPIO
import time


class DistanceSensor:

    def __init__(self, trigger, echo):
        self.trigger = trigger
        self.echo = echo
        GPIO.setup(trigger, GPIO.OUT)
        GPIO.setup(echo, GPIO.IN)
        GPIO.output(trigger, GPIO.LOW)

    #This function calculates the distance to an object in front of the sensor by multiplying the time it took for the sound made by the trigger to arrive at the echo by 17150.
    def calcDistance(self):
        GPIO.output(self.trigger, GPIO.HIGH) #activates the trigger pin
        time.sleep(0.00001)
        GPIO.output(self.trigger, GPIO.LOW)
        while GPIO.input(self.echo) == 0:
            pulse_start_time = time.time()
        while GPIO.input(self.echo) == 1:
            pulse_end_time = time.time()
        pulse_duration = pulse_end_time - pulse_start_time
        return round(pulse_duration * 17150, 2)

