import socket


class Remote:
    __instance = None
    @staticmethod
    def getInstance():  # function to get the only instance of this class since the class is a singleton
        # if there isn't an instance of this class yet, create it
        if Remote.__instance is None:
            Remote()
        # return this class's only instance
        return Remote.__instance

    def __init__(self):
        if Remote.__instance is not None:  # if the constructor of this class is called more than once
            print("Singleton class already has an instance")
        else:
            # puts the created instance in the "__instance" variable
            Remote.__instance = self
            # connection to receive data from remote
            self.HOST = "192.168.1.2"
            self.PORT = 5002
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.HOST, self.PORT))
            
            # connection to send data to remote
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

    # function to get data from the remote
    def getSignal(self):
        temp = self.s.recv(4096)
        return temp

    # function to send data to the remote
    def sendString(self, string):
        self.conn.send(string)













