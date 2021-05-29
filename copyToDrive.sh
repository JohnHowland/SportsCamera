#!/bin/bash

folder=$1
file_to_copy=$2
destination=$3
newfile=$4

echo "folder: $folder"
echo "file to copy: $file_to_copy"
echo "destination: $destination"

fullpath_before="$folder/$file_to_copy"
echo "destination_before: $fullpath"



cd $fullpath_before
cp $file_to_copy $newfile

new_filepath="$folder/$newfile"
google_drive_path="sportsCam:SportsCamVideos/$newfile"


echo "rclone copy $new_filepath $google_drive_path"

#read temp
