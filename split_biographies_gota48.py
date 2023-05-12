"""
The script reads the YAML file, loops through the letters of the Swedish alphabet, and calls the read_and_split_biographies function for each names.txt file in the "data/joined" directory. It then calls the save_biographies function, which saves each biography as a separate text file in the "data/biographies" folder. If an input file is not found, it will print a "File not found" message with the file path.

"""


import os
import re
import yaml

def read_and_split_biographies(file_name, letter):
    with open(file_name, "r", encoding="utf-8") as file:
        text = file.read()

    # Check if the letter is V, and if so, include W as an optional starting character for surnames
    pattern = fr'^({letter}[a-zåäöA-ZÅÄÖ]+),\s(?=[A-ZÅÄÖ][a-zåäö]+)'
    if letter == 'V':
        pattern = fr'^(?:[VW][a-zåäöA-ZÅÄÖ]+),\s(?=[A-ZÅÄÖ][a-zåäö]+)'

    biographies = re.split(pattern, text, flags=re.MULTILINE)[1:]

    return biographies


def save_biographies(biographies, letter):
    output_directory = 'data/biographies'
    os.makedirs(output_directory, exist_ok=True)

    for index, biography in enumerate(biographies):
        output_file_name = f'gota48_{letter}_biography_{index + 1}.txt'
        output_file_path = os.path.join(output_directory, output_file_name)

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(biography)

def main():
    with open('data/book_info/gota48_toc.yaml', 'r', encoding='utf-8') as yaml_file:
        toc = yaml.safe_load(yaml_file)

    letters = list(toc.keys())

    for letter in letters:
        input_file_name = f'gota48_{letter}-names.txt'
        input_file_path = os.path.join('data', 'joined', input_file_name)

        if os.path.isfile(input_file_path):
            biographies = read_and_split_biographies(input_file_path, letter)
            save_biographies(biographies, letter)
        else:
            print(f"File not found: {input_file_path}")

if __name__ == '__main__':
    main()
