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
    LOG_LEVEL = logging.INFO
    #LOG_LEVEL = logging.DEBUG
    LOG_FILE = "/home/pi/logs/bt_button.log"
    #LOG_FILE = "/dev/stdout"
    LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
    logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)
    logging.info("Setting up logging")

if __name__ == '__main__':
    global button_event
#    global vidcontrol
    global folder_name
    vidcontrol = cam_ctl.RaspiVidController()
    setupLogging()
    bluetoothButton = bt_btn.shutterButton("Xenvo Shutterbug   Consumer Control")
    bluetoothButton.scan_for_devices()
    bluetoothButton.connect_to_button()
  
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

    logging.debug("Blutooth Button only")
     #Loop to wait for start command
    clipLength = 10000

    logging.debug("Clip length updated to: " + str(clipLength))

    useCamera = True 
    compressFootage = False
    
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
            compressFootage = True
            break
          
        if compressFootage is True:
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
            compressFootage = False

    logging.debug("Now you are done!")
