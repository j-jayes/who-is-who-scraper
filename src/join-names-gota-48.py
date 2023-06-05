"""
The script reads the YAML file, creates the "data/joined" directory if it doesn't exist, and loops through the starting page numbers and letters of the Swedish alphabet. For each letter, it calls the join_text_files function, which reads the text files for the given page range, combines their contents, and saves the result in a new text file in the "data/joined" directory. If a file is not found, it will print a "File not found" message with the file path.

"""
import os
import yaml

def join_text_files(start_page, end_page, letter, output_directory):
    joined_text = ''

    for page_number in range(start_page, end_page):
        file_name = f'gota48_page_text_{page_number}.txt'
        file_path = os.path.join('data', 'raw', file_name)

        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                joined_text += file.read()
        else:
            print(f"File not found: {file_path}")

    output_file_name = f'gota48_{letter}-names.txt'
    output_file_path = os.path.join(output_directory, output_file_name)

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(joined_text)

def main():
    with open('data/book_info/gota48_toc.yaml', 'r', encoding='utf-8') as yaml_file:
        toc = yaml.safe_load(yaml_file)

    output_directory = 'data/joined'
    os.makedirs(output_directory, exist_ok=True)

    page_numbers = list(toc.values())
    letters = list(toc.keys())

    for i in range(len(letters)):
        start_page = page_numbers[i]
        end_page = page_numbers[i + 1] if i + 1 < len(page_numbers) else 1074
        letter = letters[i]

        join_text_files(start_page, end_page, letter, output_directory)

if __name__ == '__main__':
    main()
