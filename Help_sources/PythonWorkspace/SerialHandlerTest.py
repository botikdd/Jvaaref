
import SerialHandler
import threading,serial,time,sys


global serialHandler
A=0.3386615784101943-0.5865790603779275j
B=0.8997744537076356-0.26262039077918475j
C=0.8997744537076356+0.26262039077918475j
D=0.3386615784101943+0.5865790603779275j
timer=4.0

def testBezier(serialHandler):
    #Event test
    ev1=threading.Event()
    serialHandler.readThread.addWaiter("SPLN",ev1)
    time.sleep(2.0)
    print("Start state0")
    # sent=serialHandler.sendBezierCurve(0.5051175777578528+0.5051175777578528j,0.7840863128094306+0.22614884270627506j,0.7840863128094306-0.22614884270627506j,0.5051175777578528-0.5051175777578528j,3.0,False)
    sent=serialHandler.sendBezierCurve(A,B,C,D,timer,False)
    if sent:
        ev1.wait()
        print("Confirmed")
        
    else:
        print("Sending problem")
    print("END_TEST")
    serialHandler.readThread.deleteWaiter("SPLN",ev1)
    time.sleep(4.0)
def testMOVEAndBrake(serialHandler):
    #Event test
    ev1=threading.Event()
    serialHandler.readThread.addWaiter("MCTL",ev1)
    serialHandler.readThread.addWaiter("BRAK",ev1)
    time.sleep(1.0)
    print("Start moving")
    sent=serialHandler.sendMove(20.0,0.0)
    if sent:
        ev1.wait()
        print("Confirmed")
        
    else:
        print("Sending problem")
    time.sleep(3.0)
    print("Start braking")
    sent=serialHandler.sendBrake(0.0)
    if sent:
        ev1.wait()
        print("Confirmed")
        
    else:
        print("Sending problem")
    
    time.sleep(1.0)
    print("END_TEST")
    serialHandler.readThread.deleteWaiter("BRAK",ev1)
    serialHandler.readThread.deleteWaiter("MCTL",ev1)


def testBrake(serialHandler):
    #Event test
    ev1=threading.Event()
    serialHandler.readThread.addWaiter("BRAK",ev1)
    time.sleep(2.0)


    print("Start moving")
    for i in range(0,8):
        if i%2==0:
            sent=serialHandler.sendBrake(-20.0)
        else:
            sent=serialHandler.sendBrake(-20.0)
        if sent:
            ev1.wait()
            print("Confirmed")
            
        else:
            print("Sending problem")
        time.sleep(1)
        ev1.clear()
    
    time.sleep(1)
    # sent=serialHandler.sendBrake(0.0)
    if sent:
            ev1.wait()
            print("Confirmed")
    serialHandler.readThread.deleteWaiter("MCTL",ev1)
def testPid(SerialHandler):
    ev1=threading.Event()
    serialHandler.readThread.addWaiter("PIDA",ev1)
    time.sleep(0.1)
    sent=serialHandler.sendPidActivation(True)
    if sent:
        ev1.wait()
        print("Confirmed")
        
    else:
        print("Sending problem")
    serialHandler.readThread.deleteWaiter("PIDA",ev1)

def main():
    #Initiliazation
    global serialHandler
    serialHandler=SerialHandler.SerialHandler()
    serialHandler.startReadThread()
    testPid(serialHandler)
    # testBezier(serialHandler)
    # testBrake(serialHandler)
    testMOVEAndBrake(serialHandler)
    time.sleep(1.0)
    serialHandler.close()

if __name__=="__main__":
    main()
        