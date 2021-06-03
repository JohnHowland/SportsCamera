#!/bin/bash

folder=$1
file_to_copy=$2
destination=$3
newfile=$4

echo "folder: $folder"
echo "file to copy: $file_to_copy"
echo "destination: $destination"
echo "newfile: $newfile"

fullpath_before="$folder/$file_to_copy"
echo "destination_before: $fullpath_before"



cd \"$folder\"
cp \"$file_to_copy\" \"$newfile\"

new_filepath="$folder/$newfile"
google_drive_path="sportsCam:SportsCamVideos/$newfile"


echo "rclone copy \"$new_filepath\" \"$google_drive_path\""
read temp
