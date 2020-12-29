import os
import sys
import subprocess
import threading
import string
import RPi.GPIO as GPIO
import logging

import peripherals.camera_control as cam_ctl
import peripherals.FileStructure as CamFile
import peripherals.LED_control as led_control
import peripherals.phyical_button as button_control

def setupLogging():
    logging.basicConfig(filename='\\home\\pi\\logs\\bt_button.log', level=logging.DEBUG)
    logging.debug("Setting up logging abilities.")

#def init_vid(file, cliptime, preview):
#    global vidcontrol
#    vidcontrol = cam_ctl.RaspiVidController(file, cliptime, preview, "-fps 25 ")

#def start_vid():
#    global vidcontrol
#    vidcontrol.start()

#test program

if __name__ == '__main__':
    global button_event
#    global vidcontrol
    global folder_name
    vidcontrol = cam_ctl.RaspiVidController(file, cliptime, preview, "-fps 25 ")
    setupLogging()

    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    
    camera_file = CamFile.CameraFileSystem()
    folder_name = camera_file.initialSetup()
    
    logging.debug("folder name: %s" % folder_name)
    list_file_path = folder_name+"/list.txt"
    logging.debug("list_file_path: %s" % list_file_path)
    list_fp = open(list_file_path, "w")

    vid_index = 0
    
    list_line_out = "%d.h264" % vid_index
    list_fp.write("file "+list_line_out+"\n")
    fileName = folder_name + "/%d.h264" % vid_index
    vid_index += 1

    #Setting up buttons and LEDs
    startStopButton = button_control.button(16)
    clipLengthButton = button_control.button(18)
    captureButton = button_control.button(22)
    fiveSecondLED = led_control.LED(7)
    tenSecondLED = led_control.LED(11)
    fifteenSecondLED = led_control.LED(13)
    fiveSecondLED.setLED_off()
    tenSecondLED.setLED_off()
    fifteenSecondLED.setLED_off()

    logging.debug("Start/Stop Button: 16")
    logging.debug("Clip Length select button: 18")
    logging.debug("Capture button: 22")

     #Loop to wait for start command
    exitProgram = False
    clipLength = 10000
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

                if i == 0:
                    fiveSecondLED.setLED_on()
                    tenSecondLED.setLED_off()
                    fifteenSecondLED.setLED_off()
                elif i == 1:
                    fiveSecondLED.setLED_off()
                    tenSecondLED.setLED_on()
                    fifteenSecondLED.setLED_off()
                elif i == 2:
                    fiveSecondLED.setLED_off()
                    tenSecondLED.setLED_off()
                    fifteenSecondLED.setLED_on()

                i += 1
                logging.debug("Clip length updated to: " + str(clipLength))

                if i > 2:
                    i = 0
            
        if useCamera is True:
            vidcontrol.setupVideo(fileName, clipLength, False)

            logging.debug("Starting raspivid controller")
            vidcontrol.start()
        
        while useCamera is True:
            
            if clipLengthButton.buttonIn() == 1:
                exitProgram = True
                break

            elif startStopButton.buttonIn() == 1:
                useCamera = False
                pass

            elif captureButton.buttonIn() == 1:
                list_line_out = "%d.h264" % vid_index
                list_fp.write("file "+list_line_out+"\n")
                fileName = folder_name + "/%d.h264" % vid_index
                vid_index += 1
                vidcontrol.killCameraProcess()
          
                vidcontrol.setupVideo(fileName, clipLength, False)
                vidcontrol.start()
          
        if exitProgram is False:
            file_to_delete = vidcontrol.getCurrentFilepath()
            logging.debug("Stopping raspivid controller")
            vidcontrol.killCameraProcess()
            #os.remove(file_to_delete)

            list_fp.close()
            logging.debug("Done")

            logging.debug("Creating single file")

            mp4_out_filepath = '"'+folder_name+'/out.mp4"'
    
            os.chdir(folder_name)
            ffmpeg_out = 'ffmpeg -f concat -i list.txt -c copy out.mp4'
            logging.debug(ffmpeg_out)
    
            sub = subprocess.Popen(ffmpeg_out, shell=True)

            sub.wait() 
            logging.debug(ffmpeg_out)

    logging.debug("Now you are done!")

    fiveSecondLED.setLED_off()
    tenSecondLED.setLED_off()
    fifteenSecondLED.setLED_off()