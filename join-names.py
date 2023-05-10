
"""
This script reads a YAML file containing a table of contents for a book with chapters and page numbers,
then processes each chapter by reading the OCR text from corresponding text files in a specified directory.
For each chapter, it concatenates the text from the indicated page range and saves it to a new file in
the 'data/joined' directory. Finally, it prints a message when all chapters have been processed successfully.

Usage:
python process_chapters.py

Requires:
- A YAML file named 'toc-stockholm.yaml' in the same directory as this script.
- A directory named 'data/raw' containing the OCR text files for each page, with filenames in the
format 'sthlm_45_page_text_{page_number}.txt', where {page_number} is the page number.

Outputs:
- A directory named 'data/joined' containing the concatenated text files for each chapter, with
filenames in the format '{chapter}-names.txt', where {chapter} is the chapter name from the
YAML file.
"""


import os
import yaml

# Read the YAML file
with open('toc-stockholm.yaml', 'r') as yaml_file:
    toc = yaml.safe_load(yaml_file)

# Create the joined directory if it doesn't exist
os.makedirs('data/joined', exist_ok=True)

# Process each chapter
for chapter, pages in toc.items():
    # If only one page is listed, convert it to a range
    if isinstance(pages, int):
        pages = [pages, pages]

    start_page, end_page = pages

    # Read and join the OCR text for the specified pages
    text = ''
    for i in range(start_page, end_page + 1):
        with open(f'data/raw/sthlm_45_page_text_{i}.txt', 'r') as page_file:
            text += page_file.read() + '\n'

    # Save the joined text to a new file
    with open(f'data/joined/{chapter}-names.txt', 'w') as output_file:
        output_file.write(text)

print('All chapters processed successfully!')
