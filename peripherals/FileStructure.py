import os
import sys
import time
import datetime 

ROOT_VIDEO_DIR = "/home/pi/SportsCameraVideos"

class CameraFileSystem():
    def __init__(self):
        pass

    def initialSetup(self):
        folder_name = ROOT_VIDEO_DIR + "/" + str(datetime.datetime.now())
        folder_name.replace(' ', '_')
        os.mkdir(folder_name)
        return folder_name
