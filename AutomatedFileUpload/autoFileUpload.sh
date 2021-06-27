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

        cd $folder 
        
        new_file=( $( ls *.mp4 ) )

        new_filepath=$fileToCopy
        google_drive_path="sportsCam:SportsCamVideos/$new_file"

        pwd
        echo "rclone copy $new_fileh $google_drive_path"

        rclone copy $new_file $google_drive_path

        cd ../
    fi

done


