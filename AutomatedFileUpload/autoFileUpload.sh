#!/bin/bash

wget -q --spider http://google.com

if [ $? -eq 0 ]; then
    echo "Online"
else
    echo "Offline"
    return
fi

cd /home/pi/SportsCameraVideos

folderArray=( $( ls . ) )

for folder in "${FOLDERS[@]}"; do
    echo "Fold that "
    fileToCopy=( $( ls $folder/*.mp4 ) )
    echo "File found: $fileToCopy"
done


#rclone copy $new_filepath $google_drive_path