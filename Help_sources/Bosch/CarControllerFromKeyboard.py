import SerialHandler
import threading,serial,time,sys

global serialHandler

def main():
    #Initiliazation
    global serialHandler

    serialHandler=SerialHandler.SerialHandler()
    serialHandler.startReadThread()

    motion_event = threading.Event()
    serialHandler.readThread.addWaiter("MCTL",motion_event)
    serialHandler.readThread.addWaiter("BRAK",motion_event)

    action = ""

    speed = 0.0
    brake_speed = 0.0
    angle = 0.0

    stop = False


    try:
        while stop == False:

            sent = serialHandler.sendMove(speed, angle)

            if sent:
                motion_event.wait()
                print("Motion sent")
                
            else:
                print("Sending motion signal problem")

            action = input("Action: ")

            if action == "w" and speed <= 9.0:
                speed = speed + 1.0
                print("Speed: " + str(speed))
            elif action == "s" and speed >= 1.0:
                speed = speed - 1.0
                print("Speed: " + str(speed))
            elif action == "d" and angle <= 8.0:
                angle = angle + 2.0
                print("Angle: " + str(angle))
            elif action == "a" and angle >= 8.0:
                angle = angle - 2.0
                print("Angle: " + str(angle))

            elif action == "exit":
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
                stop = True
                        

    except KeyboardInterrupt:
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
        exit()

if __name__=="__main__":
    main()
