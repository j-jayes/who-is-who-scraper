"""
This script reads a text file containing biographies of Swedes. The format of each biography in the text file is:

Surname, first names, occupation, description, etc.

The script processes the text file and splits it into individual biographies
using a regex pattern. Then, it converts the biographies into a YAML format,
where each entry has an index for the individual and their biography details.

Finally, the script writes the resulting YAML data to an output file.

Usage:
    1. Ensure the input text file is in the same directory as this script.
    2. Run the script: `python script_name.py`
    3. The script will create a YAML file in the same directory.

Dependencies:
    - PyYAML: Required for working with YAML files in Python. Install with `pip install PyYAML`.
"""


import re
import json
import os

# Set the file paths
input_directory = "data/joined"
output_directory = "data/joined_json"

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

def read_and_split_biographies(file_name, letter):
    with open(file_name, "r", encoding="utf-8") as file:
        text = file.read()

    # Improved regex pattern to split the text
    biographies = re.split(fr'(?m)^({letter}[a-zåäöA-ZÅÄÖ]+(-[a-zåäöA-ZÅÄÖ]+)?,\s)', text)

    # Combine the split parts to form complete biographies
    combined_biographies = []
    for i in range(1, len(biographies), 2):
        name_part = biographies[i-1] if biographies[i-1] is not None else ""
        bio_part = biographies[i] if biographies[i] is not None else ""
        biography = name_part + bio_part
        combined_biographies.append(biography.strip())

    return combined_biographies

def create_json_biographies(biographies):
    # Create JSON data from the combined biographies
    json_data = {str(i): bio for i, bio in enumerate(biographies)}
    return json_data


def write_json_file(json_data, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)

def process_alphabetical_files(letters):
    for letter in letters:
        input_file = os.path.join(input_directory, f"{letter}-names.txt")
        output_file = os.path.join(output_directory, f"{letter}-names.json")

        if os.path.exists(input_file):
            biographies = read_and_split_biographies(input_file, letter)
            json_data = create_json_biographies(biographies)
            write_json_file(json_data, output_file)

if __name__ == "__main__":
    # Process files for letters A through Z, Ä, and Å
    letters = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + ['Ä', 'Å']
    process_alphabetical_files(letters)

    # Process "V & W-names.txt" file
    input_file = os.path.join(input_directory, "V & W-names.txt")
    output_file = os.path.join(output_directory, "V & W-names.json")

    if os.path.exists(input_file):
        biographies_v = read_and_split_biographies(input_file, 'V')
        biographies_w = read_and_split_biographies(input_file, 'W')
        biographies = biographies_v + biographies_w
        json_data = create_json_biographies(biographies)
        write_json_file(json_data, output_file)
