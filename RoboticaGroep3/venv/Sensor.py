from abc import ABC, abstractmethod

class Sensor(ABC):
    def onOff(self):
        return "Uit of aan"

    def getData(self):
        return "Sensor Data return"


class Sensor2(Sensor):
    def getData(self):
        return "Sensor2 data return"



r = Sensor()
print r