#!/bin/bash

# Define the directory where the files are located
directory="data/raw"

# Loop through each file in the directory
for file in "$directory"/page_text_*.txt; do
    # Check if the filename begins with "page_text_"
    if [[ $(basename "$file") == page_text_* ]]; then
        # Get the file number by removing "page_text_" and ".txt" from the filename
        number=$(basename "$file" .txt | sed 's/page_text_//')

        # Rename the file with the new name
        mv "$file" "$directory/sthlm_45_page_text_$number.txt"
    fi
done
