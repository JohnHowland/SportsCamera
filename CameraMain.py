import os
import sys
import subprocess
import threading
import time
import string
import time
import datetime 
#import bt_button
#import pygame
import camera_control as cam_ctl

#from peripherals import *
import peripherals.FileStructure as CamFile

def init_vid(file, cliptime, preview):
    global vidcontrol
    vidcontrol = cam_ctl.RaspiVidController(file, cliptime, preview, "-fps 25 ")

def start_vid():
    global vidcontrol
    vidcontrol.start()

def setupFileSystem():
    folder_name = ROOT_VIDEO_DIR + "/" + str(datetime.datetime.now())
    folder_name.replace(' ', '_')
    os.mkdir(folder_name)
    return folder_name
    

#test program

if __name__ == '__main__':
    
    global button_event
    global vidcontrol
    global folder_name

    folder_name = setupFileSystem()
    
    print("folder name: %s" % folder_name)
    list_file_path = folder_name+"/list.txt"
    print("list_file_path: %s" % list_file_path)
    list_fp = open(list_file_path, "w")

    vid_index = 0
    
    list_line_out = "%d.h264" % vid_index
    list_fp.write("file "+list_line_out+"\n")
    fileName = folder_name + "/%d.h264" % vid_index
    vid_index += 1

    #Loop to wait for start command
    exitProgram = False
    clipLength = 10000
    while exitProgram is False:
        standbyUntilInput = True
        while standbyUntilInput is True:
            x = ""
            sys.stdin.flush()
            sys.stdout.flush()
            x = input("command (<start> <quit> <clip length in seconds>): ")
            print("Received command in standbyUntilInput loop: " + str(x))

            if x == "start":
                useCamera = True
                standbyUntilInput = False

            elif x == "quit":
                useCamera = False
                exitProgram = True
                break

            elif x.isnumeric():
                if int(x) > 0 and int(x) < 30:
                    print("Updating clip length")
                    clipLength = int(x)
             
                else:
                    print("Cannot update to requested clip lendth. must be in between 1 and 30 seconds")
                
            else:
                print("Invalid input: " + str(x))

        
        if useCamera is True:
            init_vid(fileName, clipLength, False)

            print("Starting raspivid controller")
            start_vid()
        
        while useCamera is True:
            x = ""
            sys.stdin.flush()
            sys.stdout.flush()
            x = input("command (<capture> <stop> <quit>): ")

            print("Received command in useCamera loop: " + str(x))

            if x == "quit":
                exitProgram = True
                break

            elif x == "stop":
                useCamera = False
                pass

            elif x == "capture":
                list_line_out = "%d.h264" % vid_index
                list_fp.write("file "+list_line_out+"\n")
                fileName = folder_name + "/%d.h264" % vid_index
                vid_index += 1
                vidcontrol.killCameraProcess()
          
                init_vid(fileName, clipLength, False)
                start_vid()
            else:
                print("Invalid input: " + str(x))
          
        if exitProgram is False:
            file_to_delete = vidcontrol.getCurrentFilepath()
            print("Stopping raspivid controller")
            vidcontrol.killCameraProcess()
            #os.remove(file_to_delete)

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