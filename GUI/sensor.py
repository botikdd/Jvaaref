from tkinter import Canvas
from numpy import random
from utils import ranges
class Sensor:
    """
    Class to describe one sensor position and the currend data
    """

    def __init__(self, x=0, y=0, start=0):
        """
        Initializing sensor
        x: x coordinate
        y: y coordinate
        start: where it starts, in which angle, to draw the circle arc
        """
        self.x = x
        self.y = y
        self.data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.index = 0
        self.start = start
        self.arc_id = None

    def get_data(self):
        return self.data[self.index]

    def set_data(self, data):
        self.index = (self.index + 1) % 10
        self.data[self.index] = data

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
            if self.data[self.index] < rang[0]:
                return rang[1], rang[2]
        if self.data[self.index] > ranges[-1][0]:
            return ranges[-1][1], ranges[-1][2]
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
