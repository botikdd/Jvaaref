from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import datetime
import cv2
 
class PiiCamera(threading.Thread):
    def __init__(self, resolution=(384, 216)):
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.stopped = False
    def start(self):
        while self.stopped == False:
       	    picture = '/etc/img/' + str(datetime.datetime.utcnow()) + '.jpg'
       	    self.camera.capture(picture)

        if self.stopped:
            self.camera.close()
            return
 
    def stop(self):
        self.stopped = True