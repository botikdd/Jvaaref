from tkinter import Canvas
import random
from utils import ranges
class Sensor:
    """
    Class to describe one sensor position and the currend data
    """

    def __init__(self, x=0, y=0, start=0):
        self.x = x
        self.y = y
        self.data = random.randint(0, 150)
        self.start = start
        self.arc_id = None
        self.ranges = [[30, 'red', 80],\
                       [60, 'dark orange', 120],\
                       [90, 'gold', 160],\
                       [120, 'green yellow', 200],\
                       [150, 'green', 240]]

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def __draw_sensor(self, canvas=None):
        """
        Draws the sensor's location in a point format
        """
        if canvas:
            canvas.create_oval(self.x - 3, self.y - 3,\
                               self.x + 3, self.y + 3,\
                               width=10)

    def __get_color(self):
        """
        Depending on the data the sensor gives the function matches a color to
        it.
        """
        for rang in ranges:
            if self.data < rang[0]:
                return rang[1], rang[2]
        return '', 0

    def draw_sensor_data(self, canvas=None):
        """
        Draws the sensor data, an object's distance from itself
        """
        if canvas:
            if self.arc_id:
                canvas.delete(self.arc_id)
            color, radius = self.__get_color()
            self.arc_id = canvas.create_arc(self.x - radius, self.y - radius,\
                            self.x + radius, self.y + radius,\
                            start=self.start, extent=75,\
                            outline=color,\
                            width=10)
            self.__draw_sensor(canvas)
