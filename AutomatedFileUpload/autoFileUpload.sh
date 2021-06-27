#!/bin/bash

wget -q --spider http://google.com

if [ $? -eq 0 ]; then
    echo "Online"
else
    echo "Offline"
    return
fi

echo "cding now"
cd /home/pi/SportsCameraVideos

echo "getting folders in dir"
folderArray=( $( ls . ) )

echo "starting loop now"
for folder in "${folderArray[@]}"; do

    fileToCopy=( $( ls $folder/*.mp4 ) )
    
    if [ -n "$fileToCopy" ]; then
        echo "File found: $fileToCopy"

        google_drive_path="sportsCam:SportsCamVideos/$newfile"
        new_filepath=$fileToCopy

        echo "rclone copy $new_filepath $google_drive_path"

        #rclone copy $new_filepath $google_drive_path
    fi

done


