"""
This script reads a text file containing biographies of Swedes. The format of each biography in the text file is:

Surname, first names, occupation, description, etc.

The script processes the text file and splits it into individual biographies
using a regex pattern. Then, it converts the biographies into a YAML format,
where each entry has an index for the individual and their biography details.

Finally, the script writes the resulting YAML data to an output file.

Usage:
    1. Ensure the input text file "C-names.txt" is in the same directory as this script.
    2. Run the script: `python script_name.py`
    3. The script will create a YAML file named "C-names.yaml" in the same directory.

Dependencies:
    - PyYAML: Required for working with YAML files in Python. Install with `pip install PyYAML`.
"""


import re
import yaml
import os

def read_and_split_biographies(file_name, letter):
    with open(file_name, "r", encoding="utf-8") as file:
        text = file.read()

    biographies = re.split(fr'^({letter}[a-zåäöA-ZÅÄÖ]+(-[a-zåäöA-ZÅÄÖ]+)?),\s(?=[A-ZÅÄÖ][a-zåäö]+)', text, flags=re.MULTILINE)[1:]

    return biographies


def create_yaml_biographies(biographies):
    yaml_data = {}
    for i in range(0, len(biographies), 2):
        yaml_data[f"Individual {int(i/2) + 1}"] = biographies[i] + ", " + biographies[i + 1].strip()

    return yaml_data

def write_yaml_file(yaml_data, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        yaml.dump(yaml_data, file, allow_unicode=True)

def process_alphabetical_files(letters):
    for letter in letters:
        input_file = os.path.join("data", "joined", f"{letter}-names.txt")
        output_file = os.path.join("data", "joined", f"{letter}-names.yaml")

        if os.path.exists(input_file):
            biographies = read_and_split_biographies(input_file, letter)
            yaml_data = create_yaml_biographies(biographies)
            write_yaml_file(yaml_data, output_file)

if __name__ == "__main__":
    # Process files for letters A through Z, Ä, and Å
    letters = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + ['Ä', 'Å']
    process_alphabetical_files(letters)

    # Process "V & W-names.txt" file
    input_file = os.path.join("data", "joined", "V & W-names.txt")
    output_file = os.path.join("data", "joined", "V & W-names.yaml")

    if os.path.exists(input_file):
        biographies_v = read_and_split_biographies(input_file, 'V')
        biographies_w = read_and_split_biographies(input_file, 'W')
        biographies = biographies_v + biographies_w
        yaml_data = create_yaml_biographies(biographies)
        write_yaml_file(yaml_data, output_file)
