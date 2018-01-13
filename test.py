from threading import Thread, Event
from sensor import Sensor
import time
import doctest

class GetDataFromDistanceSensor(Thread):
    def __init__(self):
        """

        >>> g = GetDataFromDistanceSensor()
        >>> len(g.sensors)
        6
        """
        Thread.__init__(self)
        self.sensors = []
        self.sensors.append(Sensor(0, 0, 0))
        self.sensors.append(Sensor(0, 0, 0))
        self.sensors.append(Sensor(0, 0, 0))
        self.sensors.append(Sensor(0, 0, 0))
        self.sensors.append(Sensor(0, 0, 0))
        self.sensors.append(Sensor(0, 0, 0))

        self.stop = False

    def is_stopped(self):
        """
        Returns the stop variable's value

        >>> g = GetDataFromDistanceSensor()
        >>> g.is_stopped()
        False
        """
        return self.stop

    def set_stop(self):
        """
        Sets the stop variable's value to True, initially is False

        >>> g = GetDataFromDistanceSensor()
        >>> g.set_stop()
        True
        """
        self.stop = True
        return self.stop

    def set_sensor_data(self, data_in_string):
        """
        From a got string, splits and gets the data got from distance sensors
        """
        data = data_in_string.split(';')[:-1]
        i = 0
        for sensor_data in data:
            self.sensors[i].set_data(float(sensor_data))
            i = i + 1
        return len(data)
    
    def get_data_about_a_sensor(self, index):
        """
        Returns a specific sensors data
        
        >>> from numpy.random import randint
        >>> g = GetDataFromDistanceSensor()
        >>> g.set_sensor_data('125.2;48.6;1.24;74.69;220.3;99.56;')
        6
        >>> 1 < g.get_data_about_a_sensor(randint(5)) < 250
        True

        """
        return self.sensors[index].get_data()

if __name__ == '__main__':
    """
    >>> from numpy.random import randint
    >>> g.sensors[randint(5)].get_data()
    0.0
    """
    doctest.testmod()