#!/bin/bash

# Define the directory where the files are located
directory="data/raw"

# Loop through each file in the directory
for file in "$directory"/sthlm_45_page_text_*.txt; do
    # Check if the filename begins with "sthlm_45_page_text_"
    if [[ $(basename "$file") == sthlm_45_page_text_* ]]; then
        # Get the file number by removing "sthlm_45_page_text_" and ".txt" from the filename
        number=$(basename "$file" .txt | sed 's/sthlm_45_page_text_//')

        # Rename the file with the new name
        mv "$file" "$directory/sthlm45_page_text_$number.txt"
    fi
done
