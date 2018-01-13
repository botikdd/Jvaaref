import tkinter as tk
from PIL import ImageTk, Image
from sensor import Sensor
from socket import *
from utils import TCP_IP, TCP_PORT
import struct
import io
import time

class Application(tk.Frame):
    """
    A frame to show data from RaspberryPI
    """
    def __init__(self, master=None):
        """
        Initializing the frame
        """
        super().__init__(master)
        # setting the frame's size
        self.width = master.winfo_screenwidth() + 75
        self.height = master.winfo_screenheight() - 55
        master.geometry('{}x{}+0+0'.format(self.width, self.height))
        self.pack()

        # on the frame there will an image from the car
        self.image = None
        # the image received from care, what the camera gets
        self.photo_image = None
        self.image_label = None

        # setting elements on frame
        self.create_widgets()

        # connecting to server by socket        
        self.serversocket = None
        self.connect_to_server()

    def create_widgets(self):
        """
        Creats frames elements.
        """

        # loading image from the car
        self.image = Image.open('./Resources/audi.png')
        self.photo_image = ImageTk.PhotoImage(image=self.image)

        # putting the images to a canvas on frame
        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.canvas.pack(expand='yes', fill='both')
        self.canvas.create_image(1025, 530, image=self.photo_image)

        #  loading the image received from the camera
        self.camera_image = Image.open('./Resources/way2.png')
        self.photo_camera_image = ImageTk.PhotoImage(image=self._resize_image(self.camera_image, 600, 360))
        self.canvas.create_rectangle(800, 315, 1400, 675, width=10, outline='green')
        self.canvas.create_image(800, 315, anchor=tk.NW, image=self.photo_camera_image)

        # defining the sensors, which contains the data received from the distance sensors
        self.sensors = []
        self.sensors.append(Sensor(315, 225, 105))
        self.sensors.append(Sensor(315, 762, 180))
        self.sensors.append(Sensor(240, 330, 125))
        self.sensors.append(Sensor(240, 656, 145))
        self.sensors.append(Sensor(1650, 270, -10))
        self.sensors.append(Sensor(1650, 721, -60))

        # draw the data form distance sensors
        for sensor in self.sensors:
            sensor.draw_sensor_data(self.canvas)

    def _resize_image(self, image, width, height):
        """
        Setting the image to the given size: width x height
        """
        return image.resize((width, height))

    def refresh_loop(self):
        """
        Got actual data from server
        """
        # send reqiest to server
        self.serversocket.send(b'get')
        for sensor in self.sensors:
            # receiveing data from server
            data = self.serversocket.recv(8)
            # converting it to number format into bytes 
            (num,) = struct.unpack('d', data)
            # setting the got data to the proper sensor
            sensor.set_data(num)
            # drawing the new value
            sensor.draw_sensor_data(self.canvas)

        # receiving one block from server
        img = self.serversocket.recv(1024)
        if img == 'no'.encode():
            self.camera_image = Image.open('./Resources/way2.png')
            self.photo_camera_image = ImageTk.PhotoImage(image=self._resize_image(self.camera_image, 600, 360))
        else:
            # open a new file into which to save the image received from the server 
            with open('./Resources/imageToSave.png', 'wb') as f:
                # if this does't mark the end of stream it writes the data received to the opened file
                while not img == 'end'.encode():
                    # writing data into the file
                    f.write(img)
                    # receiving the next block
                    img = self.serversocket.recv(1024)
        # waits 0.1 second before opening it again to load it to the GUI
        time.sleep(.1)
        # opening the received image
        self.camera_image = Image.open('./Resources/imageToSave.png')
        self.photo_camera_image = ImageTk.PhotoImage(image=self._resize_image(self.camera_image, 600, 360))
        # showing it on the canvas
        self.canvas.create_rectangle(800, 315, 1400, 675, width=10, outline='green')
        self.canvas.create_image(800, 315, anchor=tk.NW, image=self.photo_camera_image)

        self.master.after(1000, self.refresh_loop)

    def connect_to_server(self):
        """
        Connecting to car with tcp sockets
        """
        self.serversocket = socket(AF_INET, SOCK_STREAM)
        self.serversocket.connect((TCP_IP, TCP_PORT))

    def disconnect_from_server(self):
        """
        Destroy connection with thw server
        """
        self.serversocket.send(b'exit')
        self.serversocket.close()

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Data From Car')
    root.configure(background='green')
    # root.attributes('-fullscreen', True)
    app = Application(master=root)
    root.after(1000, app.refresh_loop)
    app.pack(fill='both', expand='yes')
    # root.state("zoomed")
    app.mainloop()
    app.disconnect_from_server()