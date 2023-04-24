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
