from piCamera import PiiCamera
import time

camera = PiiCamera()
camera.start()

time.sleep(200)
camera.stop()
