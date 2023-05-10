"""
This script processes biographies from text files for each letter of the alphabet,
including Ä and Å, and a combined file for V and W. It splits individual biographies,
creates YAML files for each letter, and removes any page numbers between 2 and 4 digits
that appear on their own line within the biographies.

Usage:
    1. Ensure that your text files are located in the "data/joined" folder and follow
       the naming convention "{letter}-names.txt" (e.g., "A-names.txt", "B-names.txt", etc.).
    2. Run this script. It will create YAML files for each letter in the "data/joined"
       folder, following the naming convention "{letter}-names.yaml".
    3. The script will then create cleaned YAML files for each letter, removing any
       page numbers between 2 and 4 digits that appear on their own line within
       the biographies. The cleaned files follow the naming convention "{letter}-names_clean.yaml".

Functions:
    read_and_split_biographies(file_name, letter) - Reads a text file and splits individual biographies
    create_yaml_biographies(biographies) - Creates a dictionary with biographies for YAML output
    write_yaml_file(yaml_data, output_file) - Writes the YAML data to an output file
    process_alphabetical_files(letters) - Processes text files for each letter and creates YAML files
    remove_page_numbers(text) - Removes page numbers between 2 and 4 digits that appear on their own line within the text
    process_all_yaml_files(letters) - Processes all YAML files and creates cleaned versions with page numbers removed
"""

import re
import yaml
import os

def read_and_split_biographies(file_name, letter):
    with open(file_name, "r", encoding="utf-8") as file:
        text = file.read()

    biographies = re.split(fr'^({letter}[a-zåäöA-ZÅÄÖ]+),\s(?=[A-ZÅÄÖ][a-zåäö]+)', text, flags=re.MULTILINE)[1:]

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


def clean_biographies(text):
    # Remove page numbers between 2 and 4 digits that appear on their own line
    text = re.sub(r'(?<=\n)\d{2,4}(?=\n[^\n]+)', '', text, flags=re.MULTILINE)

    # Remove line breaks within each biography
    text = re.sub(r'(?<=\n\n)[\s\n]*(?=[^\n]+\n\n)', ' ', text, flags=re.MULTILINE)

    return text


def process_all_yaml_files(letters):
    for letter in letters:
        input_file = os.path.join("data", "joined", f"{letter}-names.yaml")
        output_file = os.path.join("data", "joined", f"{letter}-names_clean.yaml")

        if os.path.exists(input_file):
            with open(input_file, "r", encoding="utf-8") as file:
                yaml_text = file.read()

            clean_yaml_text = clean_biographies(yaml_text)

            with open(output_file, "w", encoding="utf-8") as file:
                file.write(clean_yaml_text)

    # Process "V & W-names.yaml" file
    input_file = os.path.join("data", "joined", "V & W-names.yaml")
    output_file = os.path.join("data", "joined", "V & W-names_clean.yaml")

    if os.path.exists(input_file):
        with open(input_file, "r", encoding="utf-8") as file:
            yaml_text = file.read()

        clean_yaml_text = clean_biographies(yaml_text)

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(clean_yaml_text)


if __name__ == "__main__":
    # Process files for letters A through Z, Ä, and Å
    letters = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + ['Ä', 'Å']
    process_alphabetical_files(letters)
    process_all_yaml_files(letters)
