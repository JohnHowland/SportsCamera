import os
import sys
import subprocess
import threading
import string
import RPi.GPIO as GPIO

import peripherals.camera_control as cam_ctl
import peripherals.FileStructure as CamFile
import peripherals.LED_control as led_control
import peripherals.phyical_button as button_control



def init_vid(file, cliptime, preview):
    global vidcontrol
    vidcontrol = cam_ctl.RaspiVidController(file, cliptime, preview, "-fps 25 ")

def start_vid():
    global vidcontrol
    vidcontrol.start()

#test program

if __name__ == '__main__':
    
    global button_event
    global vidcontrol
    global folder_name

    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    
    camera_file = CamFile.CameraFileSystem()

    folder_name = camera_file.initialSetup()
    
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

    startStopButton = button_control.button(16)
    clipLengthButton = button_control.button(18)
    captureButton = button_control.button(22)

    print("Start/Stop Button: 16")
    print("Clip Length select button: 18")
    print("Capture button: 22")

    while exitProgram is False:
        standbyUntilInput = True
        i = 0
        clipLengthArray = [5,10,15]
        clipLength = 15*1000
        while standbyUntilInput is True:
            
            if startStopButton.buttonIn() == 1:
                useCamera = True
                standbyUntilInput = False

            elif captureButton.buttonIn() == 1:
                useCamera = False
                exitProgram = True
                break

            elif clipLengthButton.buttonIn() == 1:
                clipLength = clipLengthArray[i] * 1000
                i += 1
                print("Clip length updated to: " + str(clipLength))

                if i > 2:
                    i = 0
            
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