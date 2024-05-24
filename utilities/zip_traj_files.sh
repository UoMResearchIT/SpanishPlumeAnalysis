#!/bin/bash

set -e

# Parse the parent directory from args, or use current directory
if [ $# -eq 0 ]; then
    parent_dir=$(pwd)
else
    parent_dir=$1
fi

# Save the output of the find command in an array
mapfile -t files < <(find $parent_dir -type f ! \( -name "*.pdf" -o -name "*.csv" \))

# Create a zip file with the files in the array
zip $parent_dir/$(basename $parent_dir)_trajectory_files.zip "${files[@]}"

# Delete the files
rm "${files[@]}"
# Delete empty directories
find $parent_dir -type d -empty -delete
