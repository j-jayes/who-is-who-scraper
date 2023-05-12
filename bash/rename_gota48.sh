#!/bin/bash

# Change to the data/raw directory
cd data/raw

# Loop through the range of numbers
for number in $(seq 17 1073); do
    # Old filename format
    old_filename="gota_48_page_text_${number}.txt"
    # New filename format
    new_filename="gota48_page_text_${number}.txt"

    # Rename the file
    mv "${old_filename}" "${new_filename}"
done

# Return to the original directory
cd -
