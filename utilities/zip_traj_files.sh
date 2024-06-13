#!/bin/bash

set -e

# Parse the parent directory from args, or use current directory
if [ $# -eq 0 ]; then
    parent_dir=$(pwd)
    grandparent_dir=$(dirname $parent_dir)
    cd $grandparent_dir
    parent_dir=$(basename $parent_dir)
else
    parent_dir=$1
fi

# Create an array with all the file names in parent_dir, excluding pdf, csv, zip, and mp4 files
mapfile -t files < <(find $parent_dir -type f ! \( -name "*.pdf" -o -name "*.csv" -o -name "*.zip" -o -name "*.mp4" \))

# Create a zip file with the files in the array
zip $parent_dir/$(basename $parent_dir)_trajectory_files.zip "${files[@]}"

# Delete the files
rm "${files[@]}"
# Delete empty directories
find $parent_dir -type d -empty -delete
