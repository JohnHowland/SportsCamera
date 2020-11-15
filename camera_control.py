#imports here
import os
import sys
import subprocess
import threading
import time
import string
import time
import datetime 

RASPIVIDCMD = "raspivid"
TIMETOWAITFORABORT = 0.5

#class for controlling the running and shutting down of raspivid
class RaspiVidController(threading.Thread):
    def __init__(self, filePath = "000.264h", timeout = 10000, preview = True, otherOptions=None):
        threading.Thread.__init__(self)
        
        #setup the raspivid cmd
        self.raspividcmd = RASPIVIDCMD

        #add file path, timeout and preview to options
        self.raspividcmd += ' -c -s -o "' + filePath + '" -t ' + str(timeout) + " -b 3000000 "

        if preview == False:
            self.raspividcmd += ("-n ")

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
        if raspivid.poll() == True: 
            raspivid.terminate()

    def stopController(self):
        self.running = False