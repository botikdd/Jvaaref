from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import datetime
import cv2
 
class PiiCamera:
    def __init__(self, resolution=(384, 216), cameraeffect=(128,128)):
        self.camera = PiCamera()
        self.camera.resolution = resolution
        #self.camera.color_effects = cameraeffect
        self.stopped = False
    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while self.stopped == False:
       	    picture = '/etc/img/' + str(datetime.datetime.utcnow()) + '.png'
       	    self.camera.capture(picture)

        if self.stopped:
            self.camera.close()
            return
 
    def _stop(self):
        self.stopped = True
