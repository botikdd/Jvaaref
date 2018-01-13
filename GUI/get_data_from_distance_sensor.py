import SerialHandler
from threading import Thread, Event
from sensor import Sensor
import time

class GetDataFromDistanceSensor(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.sensors = []
        self.sensors.append(Sensor(0, 0, 0))
        self.sensors.append(Sensor(0, 0, 0))
        self.sensors.append(Sensor(0, 0, 0))
        self.sensors.append(Sensor(0, 0, 0))
        self.sensors.append(Sensor(0, 0, 0))
        self.sensors.append(Sensor(0, 0, 0))

        self.stop = False
        self.serialHandler = SerialHandler.SerialHandler()
        self.serialHandler.startReadThread()
        self.proximityInputEvent = Event()
        self.serialHandler.readThread.addWaiter("DSPB", self.proximityInputEvent, self.set_sensor_data)

    def is_stopped(self):
        """
        Returns the stop variable's value
        """
        return self.stop

    def set_stop(self):
        """
        Sets the stop variable's value to True, initially is False
        """
        self.stop = True

    def set_sensor_data(self, data_in_string):
        """
        
        """
        data = data_in_string.split(';')
        print(data)
        print()

if __name__ == '__main__':
    th = GetDataFromDistanceSensor()
    th.start()
