import os
import sys
import time

ROOT_VIDEO_DIR = "/home/pi/SportsCameraVideos"

class CameraFileSystem():
    def __init__():
        pass

    def initialSetup():
        folder_name = ROOT_VIDEO_DIR + "/" + str(datetime.datetime.now())
        folder_name.replace(' ', '_')
        os.mkdir(folder_name)
        return folder_name
