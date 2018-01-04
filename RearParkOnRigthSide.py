import SerialHandler
import threading,serial,time,sys

global serialHandler

def sendMotion(serialHandler, motion_event, speed, angle, time_to_sleep):
    sent = serialHandler.sendMove(speed, angle)

    if sent:
        motion_event.wait()
        print("Motion sent")
        
    else:
        print("Sending motion signal problem")
        return None

    time.sleep(time_to_sleep)

def main():
    #Initiliazation
    global serialHandler

    serialHandler=SerialHandler.SerialHandler()
    serialHandler.startReadThread()

    motion_event = threading.Event()
    serialHandler.readThread.addWaiter("MCTL",motion_event)
    serialHandler.readThread.addWaiter("BRAK",motion_event)

    speed = 8.3
    angle = 25.0
    time = 1.0

    sendMotion(serialHandler, motion_event, speed, angle, time)

    speed = -8.3
    angle = -25.0
    time = 1.3

    sendMotion(serialHandler, motion_event, speed, angle, time)

    speed = 8.3
    angle = 25.0
    time = 2.5

    sendMotion(serialHandler, motion_event, speed, angle, time)

    speed = 8.3
    angle = 0.0
    time = 0.2

    sendMotion(serialHandler, motion_event, speed, angle, time)

    brake_speed = 0.0

    sent = serialHandler.sendBrake(brake_speed)
    if sent:
        motion_event.wait()
        print("Braking sent")
        
    else:
        print("Sending brake signal problem")
    print("KeyboardInterrupt Exception, wait 5 seconds for the serial handler to close connection")
    time.sleep(5.0)
    serialHandler.readThread.deleteWaiter("BRAK",motion_event)
    serialHandler.readThread.deleteWaiter("MCTL",motion_event)
    serialHandler.close()

main()
