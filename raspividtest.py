import os
import sys
import subprocess
import threading
import time
import string
import time
import datetime 
import bt_button
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

def init_vid(file):
    global vidcontrol
    vidcontrol = RaspiVidController(file, 10000, True, "-fps 25 ")

def start_vid():
    global vidcontrol
    vidcontrol.start()

def stop_vid():
    global vidcontrol
    #stop the controller
    vidcontrol.stopController()
    #wait for the tread to finish if it hasn't already
    vidcontrol.join()
    #threading.Thread.__init__()
    subprocess.Popen("kill -USR1 `pidof raspivid`", shell=True)

def setupFileSystem():
    print("This is where setting up the file path will go")
        
    
ROOT_VIDEO_DIR = "/home/pi/SportsCameraVideos"

#test program
if __name__ == '__main__':

    setupFileSystem()

    folder_name = ROOT_VIDEO_DIR + "/" + str(datetime.datetime.now())
    folder_name.replace(' ', '_')
    os.mkdir(folder_name)
    
    print("folder name: %s" % folder_name)
    list_file_path = folder_name+"/list.txt"
    print("list_file_path: %s" % list_file_path)
    list_fp = open(list_file_path, "w")

    vid_index = 0
    
    list_line_out = "%d.h264" % vid_index
    list_fp.write("file "+list_line_out+"\n")
    fileName = folder_name + "/%d.h264" % vid_index
    vid_index += 1
    init_vid(fileName)

    print("Starting raspivid controller")
    start_vid()
    
    while 1:
        x = ""
        sys.stdin.flush()
        sys.stdout.flush()
        x = input("command: ")

        print("received command: " + str(x))

        if x == "exit":
            break
        elif x == "capture":
            list_line_out = "%d.h264" % vid_index
            list_fp.write("file "+list_line_out+"\n")
            fileName = folder_name + "/%d.h264" % vid_index
            vid_index += 1
            stop_vid()
            time.sleep(1.0)
            init_vid(fileName)
            start_vid()
        else:
            print("Invalid event: " + str(x))
          

    print("Stopping raspivid controller")
    stop_vid()
    list_fp.close()
    print("Done")

    print("Creating single file")

    mp4_out_filepath = '"'+folder_name+'/out.mp4"'
    
    os.chdir(folder_name)
    ffmpeg_out = 'ffmpeg -f concat -i list.txt -c copy out.mp4'
    print(ffmpeg_out)
    
    sub = subprocess.Popen(ffmpeg_out, shell=True)

    sub.wait() 
    print(ffmpeg_out)
    print("Now you are done!")