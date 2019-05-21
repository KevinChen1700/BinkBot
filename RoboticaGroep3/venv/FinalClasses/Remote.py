import socket
#import RPi.GPIO as GPIO

class Remote:
    __instance = None
    @staticmethod
    def getInstance():
        if Remote.__instance == None:
            Remote()
        return Remote.__instance

    def __init__(self):
        if Remote.__instance != None:
            print("Singleton class already has an instance")
        else:
            Remote.__instance = self
            HOST = "141.252.230.54"
            PORT = 5002
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #this.s.connect((HOST, PORT))
            self.needsUpdate = False
            self.lastpressed = "test"

    def getSignal(self):
        temp = self.s.recv(50)
        if self.lastpressed == temp:
            self.needsUpdate = True
            self.lastpressed = temp





