import SerialHandler
import threading,serial,time,sys

global serialHandler

def main():
    #Initiliazation
    global serialHandler

    serialHandler=SerialHandler.SerialHandler()
    serialHandler.startReadThread()

    motion_event = threading.Event()
    serialHandler.readThread.addWaiter("DSPB",motion_event)

    sent = serialHandler.sendProximityRequest(True)


    time.sleep(30)
    sent = serialHandler.sendProximityRequest(False)


if __name__=="__main__":
    main()
