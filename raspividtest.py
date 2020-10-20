import os
import subprocess
import threading
import time
#import pygame

RASPIVIDCMD = "raspivid"
TIMETOWAITFORABORT = 0.5

#class for controlling the running and shutting down of raspivid
class RaspiVidController(threading.Thread):
    def __init__(self, filePath = "000.264h", timeout = 10000, preview = True, otherOptions=None):
        threading.Thread.__init__(self)
        
        #setup the raspivid cmd
        self.raspividcmd = RASPIVIDCMD

        #add file path, timeout and preview to options
        self.raspividcmd += " -o"
        self.raspividcmd += " " + filePath
        self.raspividcmd += (" -t ")
        self.raspividcmd += str(timeout)

        if preview == False:
            self.raspividcmd += (" -n ")

        #if there are other options, add them
        if otherOptions != None:
            self.raspividcmd = self.raspividcmd + otherOptions

        #set state to not running
        self.running = False
        
    def run(self):
        #run raspivid
        print("subprocess string:  " + str(self.raspividcmd))
        raspivid = subprocess.Popen(self.raspividcmd, shell=True)
        
        #loop until its set to stopped or it stops
        self.running = True
        while(self.running and raspivid.poll() is None):
            time.sleep(TIMETOWAITFORABORT)
        self.running = False
        
        #kill raspivid if still running
        if raspivid.poll() == True: raspivid.terminate()

    def stopController(self):
        self.running = False

def init_vid():
    global vidcontrol
    vidcontrol = RaspiVidController("/home/pi/test.h264", 10000, True, "-fps 25 ")

def start_vid():
    global vidcontrol
    vidcontrol.start()

def stop_vid():
    global vidcontrol
    #stop the controller
    vidcontrol.stopController()
    #wait for the tread to finish if it hasn't already
    vidcontrol.join()

#test program
if __name__ == '__main__':

    init_vid()

    print "Starting raspivid controller"
    start_vid()
    time.sleep(5)
    print "Stopping raspivid controller"
    stop_vid()
    print "Done"