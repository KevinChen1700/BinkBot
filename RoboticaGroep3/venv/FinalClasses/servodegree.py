from AX12 import Ax12
from time import sleep

servos = Ax12()

while True:
    print("Servo 1: " + str(servos.readPosition(1)) + " Servo 2: " + str(servos.readPosition(2))+ " Servo 3: " + str(servos.readPosition(3)) + " Servo 4: " + str(servos.readPosition(4)))
    sleep(0.8)


##def mapdeg(x):
##    return (int)((x - 30) * (1023 - 0) / (330 - 30));
##
##def mapdegtest(x):
##    return (int)((x + 30) / (1023 - 0) * (330 - 30));
##
##print(str(mapdeg(10)))

##x = 0
##while True:
##    print(str(mapdeg(x)))
##    x = x+1
##    print("x is " + str(x) + " 534 was het getal")
##    sleep(0.01)
