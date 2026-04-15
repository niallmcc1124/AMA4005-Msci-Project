#!/bin/bash
##CLEAR DIRECTORIES
###BE CAREFUL, THIS WILL DELETE ALL FILES IN THE SUBDIRECTORIES OF THE GIVEN PARENT DIRECTORY
###To use: ./Clear_Directories.sh <parent-directory> 
### ONlY WHEN it has all gone wrong and you want to start from scratch.
parent="$1"

if [ -z "$parent" ]; then
    echo "Usage: $0 <parent-directory>"
    exit 1
fi

parent="$(readlink -f "$parent")"

for dir in "$parent"/*/; do
    [ -d "$dir" ] || continue
    echo "Clearing: $dir"
    rm -rf "$dir"/* "$dir"/.[!.]* "$dir"/..?*
done


#!/bin/bash
##MAKE NEW FOLDERS
###Creates the new folders that you had before, but now empty. You can use this after running the Clear_Directories.sh script to start fresh.
###To use: ./Make_Folders.sh <parent-directory>
parent="$1"

if [ -z "$parent" ]; then
    echo "Usage: $0 <parent-directory>"
    exit 1
fi

parent="$(readlink -f "$parent")"

# List of folders you want to create inside each seed directory
folders=("T9A_P" "T9A_S" "T9A_R" "T9A_T")

for dir in "$parent"/*/; do
    [ -d "$dir" ] || continue
    echo "Creating folders inside: $dir"

    for f in "${folders[@]}"; do
        mkdir -p "$dir/$f"
    done
done
