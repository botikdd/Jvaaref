from piCamera import PiiCamera
import time

camera = PiiCamera()
camera.start()


sleep(10)

camera.stop()