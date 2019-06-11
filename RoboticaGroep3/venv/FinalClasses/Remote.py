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
            self.HOST = "141.252.29.24"
            self.PORT = 5002
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.HOST, self.PORT))
            self.needsUpdate = False
            self.lastpressed = "test"

    def getSignal(self):
        temp = self.s.recv(4096)
        if not self.lastpressed == temp:
            self.needsUpdate = True
            self.lastpressed = temp
        return self.lastpressed






