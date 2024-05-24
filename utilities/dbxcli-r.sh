#!/bin/bash

set -e

# Check if two arguments are provided
if [ "$#" -lt 3 ]; then
    echo """
    Usage:    dbxcli-r <put/get> <source_directory> <dropbox_directory> [--dry-run]

    This script helps to recursively upload/download files from/to Dropbox using dbxcli.
    
    Example:
        A directory with this structure:
            .
            ├── Documents
            │   ├── My_Dir
            │   │   ├── SubDir1
            |   |   |   ├── file1.txt
            |   |   |   ├── file2.txt
            │   │   ├── SubDir2
            |   |   |   ├── file3.txt
            |   |   |   ├── file4.txt
        Can be uploaded to Dropbox as:
            .
            ├── Documents
            │   ├── Uploaded_Dir
            │   │   ├── SubDir1
            |   |   |   ├── file1.txt
            |   |   |   ├── file2.txt
            │   │   ├── SubDir2
            |   |   |   ├── file3.txt
            |   |   |   ├── file4.txt
        Using the command:

            dbxcli-r put Documents/My_Dir /Documents/Uploaded_Dir
        
    The --dry-run option can be used to print the commands that would be executed without actually executing them.

    Note: The 'get' command is not yet implemented.
    """
    exit 1
fi

# Assign arguments to variables
COMMAND="$1"
SOURCE_DIR="${2%/}"
DEST_DIR="${3%/}"
# Check for options 
DRY_RUN="false"
if [ "$#" == 4 ]; then
    if [ "$4" == "--dry-run" ]; then
        DRY_RUN="true"
    fi
fi

# Make sure command is either put or get
if [ "${COMMAND}" != "put" ] && [ "${COMMAND}" != "get" ]; then
    echo "Command must be either 'put' or 'get'"
    exit 1
fi
if [ "${COMMAND}" == "put" ]; then
    # Make sure the source directory exists
    if [ ! -d "${SOURCE_DIR}" ]; then
        echo "Source directory does not exist"
        exit 1
    fi
    # if dry-run option specified, just echo the commands
    if [ "${DRY_RUN}" == "true" ]; then
        echo "----- DRY RUN -----"
    fi
    echo "Uploading files from \""${SOURCE_DIR}"\" to \""${DEST_DIR}"\"..."
    find "${SOURCE_DIR}" -type f -exec bash -c 'dir=$(dirname "${1#${2}}"); if [ "$dir" == "/" ]; then dir=""; fi; echo dbxcli put \""$1"\" \""${3}${dir}/$(basename "$1")"\"' _ {} "${SOURCE_DIR}" "${DEST_DIR}" \;
    if [ "${DRY_RUN}" != "true" ]; then
        # Put each file recursively
        find "${SOURCE_DIR}" -type f -exec bash -c 'dir=$(dirname "${1#${2}}"); if [ "$dir" == "/" ]; then dir=""; fi; dbxcli put "$1" "${3}${dir}/$(basename "$1")"' _ {} "${SOURCE_DIR}" "${DEST_DIR}" \;
    else
        echo "-------------------"
    fi
fi
if [ "${COMMAND}" == "get" ]; then
    echo "This is not implemented yet"
fi
