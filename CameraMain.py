import os
import sys
import subprocess
import threading
import string
import RPi.GPIO as GPIO
import logging
import time
import datetime

import peripherals.camera_control as cam_ctl
import peripherals.FileStructure as CamFile
import peripherals.LED_control as led_control
import peripherals.phyical_button as button_control
import peripherals.bt_button as bt_btn

def setupLogging():
    pass

def rename_and_copy_file(selectedFolder, selectedFile):
    new_file_name = str(datetime.datetime.now())+".mp4"
    new_file_name = new_file_name.replace(" ", "_")

    print(f"selectedFolder: {selectedFolder}, selectedFile: {selectedFile}, new_file_name: {new_file_name}")
    rc = subprocess.Popen(['/home/pi/dev/SportsCamera/copyToDrive.sh', selectedFolder, selectedFile, "nothing", new_file_name])   #, stdout=subprocess.PIPE
    rc.wait()
    pass

if __name__ == '__main__':
    #LOG_LEVEL = logging.INFO
    LOG_LEVEL = logging.DEBUG
    LOG_FILE = "/home/pi/logs/bt_button.log"
    #LOG_FILE = "/dev/stdout"
    LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
    logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)
    logging.info("Setting up logging")

    global button_event
#    global vidcontrol
    global folder_name
    vidcontrol = cam_ctl.RaspiVidController()
    setupLogging()

    connecting = False
    while connecting is False:
        bluetoothButton = bt_btn.shutterButton("Xenvo Shutterbug   Consumer Control")
        bluetoothButton.scan_for_devices()
        connecting = bluetoothButton.connect_to_button()

    #TODO: Need to add error checking around when button is there to connect
  
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

             #copy file to the google drive here
            #need to check to internet connection
            rename_and_copy_file(folder_name, "out.mp4")


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

            vidcontrol.setupVideo(fileName, clipLength, False)

            logging.debug("Starting raspivid controller")
            vidcontrol.start()
            compressFootage = False



    logging.debug("Now you are done!")
