#!/bin/bash

# Loop over all the text files in the "data/raw" folder
for file in data/raw/sthlm_45_page_text_*.txt; do
    # Use sed to remove the </br> tag from the beginning of a line
    sed -i 's#^<br/>##g' "$file"
done
