import socket
from Microphone import Microphone

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
            #connection to send data to remote
            self.s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.s2.connect(("8.8.8.8", 80))
            self.HOST = self.s2.getsockname()[0]
            self.PORT = 5002
            print self.HOST
            self.s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s2.bind((self.HOST, self.PORT))
            self.s2.listen(1)
            self.conn, self.addr = self.s2.accept()
            self.s2.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            print 'Connected by', self.addr

            #connection to receive data from remote
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

    def sendBatteryValue(self):
        value = str(self.Microphone.getBattery())
        self.conn.send(value)
        print(value)







