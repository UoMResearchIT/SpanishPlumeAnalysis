#!/bin/bash

# Starting from a directory structure like this:
# 024-04_SkewT_SLP/
# ├── SkewT
# │   ├── Control
# │   │   ├── __SkewT_Aberporth
# │   │   |   ├── SkewT_Aberporth_01.pdf
# │   │   |   ├── SkewT_Aberporth_02.pdf
# │   │   ├── __SkewT_Algeria
# │   │   |   ├── SkewT_Algeria_01.pdf
# │   │   |   ├── SkewT_Algeria_02.pdf
# │   │   ├── SkewT_Aberporth.mp4
# │   │   ├── SkewT_Algeria.mp4
# │   ├── Albedo_90
# │   │   ├── __SkewT_Aberporth
# │   │   |   ├── SkewT_Aberporth_01.pdf
# │   │   |   ├── SkewT_Aberporth_02.pdf
# │   │   ├── __SkewT_Algeria
# │   │   |   ├── SkewT_Algeria_01.pdf
# │   │   |   ├── SkewT_Algeria_02.pdf
#
# This script will compress all the pdf files in the directories starting 
# with "__" into files named "xxx_frames.zip", and then delete the original,
# so the directory structure will look like this:
# 024-04_SkewT_SLP/
# ├── SkewT
# │   ├── Control
# │   │   ├── SkewT_Aberporth.mp4
# │   │   ├── SkewT_Aberporth_frames.zip
# │   │   ├── SkewT_Algeria.mp4
# │   │   ├── SkewT_Algeria_frames.zip
# │   ├── Albedo_90
# │   │   ├── SkewT_Aberporth.mp4
# │   │   ├── SkewT_Aberporth_frames.zip
# │   │   ├── SkewT_Algeria.mp4
# │   │   ├── SkewT_Algeria_frames.zip

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


# # Create a test directory structure
# mkdir test_parent_dir
# cd test_parent_dir
# 
# mkdir -p S1/C1/__A
# touch S1/C1/__A/S1_C1_A1.pdf
# touch S1/C1/__A/S1_C1_A2.pdf
# touch S1/C1/__A/S1_C1_A3.pdf
# mkdir -p S1/C1/A.mp4
# 
# mkdir -p S1/C1/__B
# touch S1/C1/__B/S1_C1_B1.pdf
# touch S1/C1/__B/S1_C1_B2.pdf
# touch S1/C1/__B/S1_C1_B3.pdf
# mkdir -p S1/C1/B.mp4
# 
# mkdir -p S1/C2/__A
# touch S1/C2/__A/S1_C2_A1.pdf
# touch S1/C2/__A/S1_C2_A2.pdf
# touch S1/C2/__A/S1_C2_A3.pdf
# mkdir -p S1/C2/B.mp4
# 
# mkdir -p S1/C2/__B
# touch S1/C2/__B/S1_C2_B1.pdf
# touch S1/C2/__B/S1_C2_B2.pdf
# touch S1/C2/__B/S1_C2_B3.pdf
# mkdir -p S1/C2/A.mp4
# 
# touch S1/C1/C.mp4
# touch S1/C2/C.txt
# 
# mkdir -p S2/C1/__A
# touch S2/C1/__A/S2_C1_A1.pdf
# touch S2/C1/__A/S2_C1_A2.pdf
# touch S2/C1/__A/S2_C1_A3.pdf
# mkdir -p S2/C1/A.mp4
# 
# mkdir -p S2/C1/__B
# touch S2/C1/__B/S2_C1_B1.pdf
# touch S2/C1/__B/S2_C1_B2.pdf
# touch S2/C1/__B/S2_C1_B3.pdf
# mkdir -p S2/C1/B.mp4
# 
# mkdir -p S2/C2/__A
# touch S2/C2/__A/S2_C2_A1.pdf
# touch S2/C2/__A/S2_C2_A2.pdf
# touch S2/C2/__A/S2_C2_A3.pdf
# mkdir -p S2/C2/B.mp4
# 
# mkdir -p S2/C2/__B
# touch S2/C2/__B/S2_C2_B1.pdf
# touch S2/C2/__B/S2_C2_B2.pdf
# touch S2/C2/__B/S2_C2_B3.pdf
# mkdir -p S2/C2/A.mp4
# 
# touch S2/C1/C.mp4
# touch S2/C2/C.txt
