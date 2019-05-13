import RPi.GPIO as GPIO
from time import sleep

PWM1 = 13 #motor1 snelheid 
PWM2 = 18 #motor2 snelheid   
INA1 = 5 #richting a motor 1
INB1 = 6 #richting b motor 1
INA2 = 23 #richting a motor 2
INB2 = 24 #richting b motor 2

running = True
minsnelheid = 12

GPIO.setwarnings(False)#gpio waarschuwingen uit
GPIO.setmode(GPIO.BCM)#pinmode instellen
GPIO.setup(PWM1, GPIO.OUT)#instellen als in/uitgangen
GPIO.setup(PWM2, GPIO.OUT)
GPIO.setup(INA1, GPIO.OUT)
GPIO.setup(INB1, GPIO.OUT)
GPIO.setup(INA2, GPIO.OUT)
GPIO.setup(INB2, GPIO.OUT)


VM1 = GPIO.PWM(PWM1, 100)#freq. instellen
VM2 = GPIO.PWM(PWM2, 100)
VM1.start(0)#start dutycycle instellen
VM2.start(0)

def MOTOR1(richting1, snelheid1):
    if richting1 == 1:  #motor1 rechts
        GPIO.output(INA1, 1) #ina op 1 instellen inb op 0, zodat motor naar rechts draait
        GPIO.output(INB1, 0)
        sleep(0.01) #wacht 10ms
        if snelheid1 >= minsnelheid: #beveiliging voor te lage snelheid
            VM1.ChangeDutyCycle(snelheid1) #nieuwe snelheid als pwm instellen
        print('Rechts M1') #print snelheid
    if richting1 == 0:  #motor1 links
        GPIO.output(INA1, 0)
        GPIO.output(INB1, 1)
        sleep(0.01)
        if snelheid1 >= minsnelheid:
            VM1.ChangeDutyCycle(snelheid1)
        print('Links M1') 

def MOTOR2(richting2, snelheid2):
    if richting2 == 1: #motor2 rechts
        GPIO.output(INA2, 1)
        GPIO.output(INB2, 0)
        sleep(0.01)
        VM2.ChangeDutyCycle(snelheid2)
        print('Rechts M2')
    if richting2 == 0:  #motor2 links
        GPIO.output(INA2, 0)
        GPIO.output(INB2, 1)
        sleep(0.01)
        VM2.ChangeDutyCycle(snelheid2)
        print('Links M2')

def main():
    MOTOR1(0, 100)#fucntie aanroepen met richting en snelheid
    MOTOR2(0, 70)

try:
    while True:
        main()
    
except KeyboardInterrupt: #stop als knop word ingedrukt
    print("Exit Button pressed")

finally:
    print('exit1')
    VM1.stop() #stop pwm signaal
    VM2.stop()
    GPIO.cleanup() #pins resseten
        
print('exit2')

    
