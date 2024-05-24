#!/bin/bash

set -e

# Parse the parent directory from args, or use current directory
if [ $# -eq 0 ]; then
    parent_dir=$(pwd)
else
    parent_dir=$1
fi

# Search for directories starting with "__"

for dir in $(find $parent_dir -type d -name "__*"); do
    # Get the directory name
    dir_name=$(basename $dir)
    # Remove the "__" prefix
    dir_name=${dir_name:2}
    # Get the parent directory
    parent_dir=$(dirname $dir)
    # Create a zip file with the same name as the directory
    zip -j $parent_dir/${dir_name}_frames.zip $dir/*.pdf
    # Remove the original directory
    rm -r $dir
done
