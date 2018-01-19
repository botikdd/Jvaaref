from picamera.array import PiRGBArray
from picamera import PiCamera
import threading
import datetime
import cv2
 
class PiiCamera():
    def __init__(self, resolution=(384, 216), targetdir='/etc/img/'):
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.targetdir = targetdir
        self.stopped = False
        #self.camera.color_effects = (128,128)
    def start(self):
        threading.Thread(target=self.update).start()
    def update(self):
        while self.stopped == False:
            picture = self.targetdir + str(datetime.datetime.utcnow()) + '.png'
            self.camera.capture(picture)
            if self.stopped:
                self.camera.close()
                return
    def stop(self):
        self.stopped = True
