import re
import os
import json
from string import ascii_uppercase

# Function to split a file into chunks based on the specified chunk size
def split_biographies(file_path, letter, chunk_size=50):
    pattern = re.compile(fr'(?m)^({letter}[a-zåäöA-ZÅÄÖ]+(-[a-zåäöA-ZÅÄÖ]+)?,\s)')

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    chunks = []
    current_chunk = []
    line_count = 0

    for line in lines:
        if pattern.match(line) and line_count >= chunk_size:
            chunks.append(current_chunk)
            current_chunk = [line]
            line_count = 1
        else:
            current_chunk.append(line)
            line_count += 1

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

# Main function to process, save files in JSON, and also save each chunk to a text file
def process_and_save_files():
    base_folder = 'data/joined'

    for folder_name in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder_name)
        if os.path.isdir(folder_path):
            for letter in ascii_uppercase:
                file_path = os.path.join(folder_path, f'{folder_name}_{letter}-names.txt')

                if os.path.exists(file_path):
                    chunks = split_biographies(file_path, letter)
                    chunk_strings = {str(i): ''.join(chunk) for i, chunk in enumerate(chunks)}

                    # Directories for text files
                    text_output_dir = os.path.join('data/joined_text', folder_name, letter)
                    os.makedirs(text_output_dir, exist_ok=True)

                    # Directories for JSON files
                    json_output_dir = os.path.join('data/joined_json', folder_name, letter)
                    os.makedirs(json_output_dir, exist_ok=True)

                    # Saving JSON file
                    with open(os.path.join(json_output_dir, f'{folder_name}_{letter}_chunks.json'), 'w', encoding='utf-8') as f:
                        json.dump(chunk_strings, f, ensure_ascii=False, indent=4)

                    # Saving each chunk to a separate text file
                    for index, chunk in chunk_strings.items():
                        with open(os.path.join(text_output_dir, f'{folder_name}_{letter}_{index}.txt'), 'w', encoding='utf-8') as text_file:
                            text_file.write(chunk)

# Usage example:
process_and_save_files()