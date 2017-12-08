from PIL import ImageTk, Image
import tkinter as tk
from sensor import Sensor
import random as rnd

class Application(tk.Frame):
    """
    A frame to get data from RaspberryPI
    """
    def __init__(self, master=None):
        """
        Initializing the frame
        """
        super().__init__(master)
        self.width = master.winfo_screenwidth() + 75
        self.height = master.winfo_screenheight() - 55
        master.geometry('{}x{}+0+0'.format(self.width, self.height))
        self.pack()

        self.image = None
        self.photo_image = None
        self.image_label = None

        self.create_widgets()

    def create_widgets(self):
        """
        Creats frames elements.
        """
        # self.quit = tk.Button(self, text='QUIT', fg='red',\
        #                       command=root.destroy)
        # self.quit.pack(side='top')

        self.image = Image.open('./Resources/audi.png')
        self.photo_image = ImageTk.PhotoImage(image=self.image)

        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.canvas.pack(expand='yes', fill='both')
        self.canvas.create_image(1025, 530, image=self.photo_image)

        self.camera_image = Image.open('./Resources/way.png')
        self.photo_camera_image = ImageTk.PhotoImage(image=self._resize_image(self.camera_image, 600, 360))
        self.canvas.create_rectangle(800, 315, 1400, 675, width=10, outline='green')
        self.canvas.create_image(800, 315, anchor=tk.NW, image=self.photo_camera_image)

        self.sensors = []
        self.sensors.append(Sensor(315, 225, 105))
        self.sensors.append(Sensor(315, 762, 180))
        self.sensors.append(Sensor(240, 330, 125))
        self.sensors.append(Sensor(240, 656, 145))
        self.sensors.append(Sensor(1650, 270, -10))
        self.sensors.append(Sensor(1650, 721, -60))

        for sensor in self.sensors:
            sensor.draw_sensor_data(self.canvas)

    def _resize_image(self, image, width, height):
        """
        Setting the image to the given size: width x height
        """
        return image.resize((width, height))

    def refresh_loop(self):
        for sensor in self.sensors:
            sensor.set_data(rnd.randint(0, 150))
            sensor.draw_sensor_data(self.canvas)
        self.master.after(1000, self.refresh_loop)

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