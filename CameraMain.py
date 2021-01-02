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
import peripherals.bt_button as bt_btn

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
#    vidcontrol = cam_ctl.RaspiVidController(file, cliptime, preview, "-fps 25 ")
    setupLogging()
    bluetoothButton = bt_btn.shutterButton("Xenvo Shutterbug   Consumer Control")
    bluetoothButton.scan_for_devices()
    bluetoothButton.connect_to_button()

#    GPIO.setwarnings(False) # Ignore warning for now
#    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    
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
#    startStopButton = button_control.button(16)
#    clipLengthButton = button_control.button(18)
#    captureButton = button_control.button(22)
#    fiveSecondLED = led_control.LED(7)
#    tenSecondLED = led_control.LED(11)
#    fifteenSecondLED = led_control.LED(13)
#    fiveSecondLED.setLED_off()
#    tenSecondLED.setLED_off()
#    fifteenSecondLED.setLED_off()

#    logging.debug("Start/Stop Button: 16")
#    logging.debug("Clip Length select button: 18")
#    logging.debug("Capture button: 22")

    logging.debug("Blutooth Button only")
     #Loop to wait for start command
    clipLength = 10000

    logging.debug("Clip length updated to: " + str(clipLength))

    useCamera = True     
    
    if useCamera is True:
        vidcontrol.setupVideo(fileName, clipLength, False)

        logging.debug("Starting raspivid controller")
        vidcontrol.start()
        
    while useCamera is True:
        button_input = bluetoothButton.get_events()

        if button_input == "single":
            list_line_out = "%d.h264" % vid_index
            list_fp.write("file "+list_line_out+"\n")
            fileName = folder_name + "/%d.h264" % vid_index
            vid_index += 1
            vidcontrol.killCameraProcess()
          
            vidcontrol.setupVideo(fileName, clipLength, False)
            vidcontrol.start()
        elif button_input == "long":
            exitProgram = True
          
    if exitProgram is False:
        file_to_delete = vidcontrol.getCurrentFilepath()
        logging.debug("Stopping raspivid controller")
        vidcontrol.killCameraProcess()

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