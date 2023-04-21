# pip install pytesseract opencv-python-headless Pillow

import cv2
import pytesseract
from PIL import Image
from pytesseract import Output
import os

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path

def extract_biographies(image_path):
    # Read the image and convert to grayscale
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply some pre-processing to improve OCR accuracy
    gray = cv2.medianBlur(gray, 3)

    # Perform OCR using Tesseract
    custom_config = r'--oem 3 --psm 6'  # psm 6 works well for two-column layouts
    d = pytesseract.image_to_data(gray, output_type=Output.DICT, config=custom_config)

    # Extract words and their boldness
    words = []
    for i in range(len(d['text'])):
        word = d['text'][i].strip()
        is_bold = d['fontname'][i].endswith('Bold')

        if word and is_bold:
            words.append((word, is_bold))

    # Split biographies based on boldness and indentation
    biographies = []
    current_bio = []
    for word, is_bold in words:
        if is_bold and not current_bio:
            current_bio.append(word)
        elif is_bold and current_bio:
            biographies.append(' '.join(current_bio))
            current_bio = [word]
        else:
            current_bio.append(word)

    if current_bio:
        biographies.append(' '.join(current_bio))

    return biographies



def extract_biographies_to_file(image_path):
    biographies = extract_biographies(image_path)

    # Create the output folder if it doesn't exist
    output_folder = 'data/raw-images'
    os.makedirs(output_folder, exist_ok=True)

    # Set the output file path
    filename = os.path.splitext(os.path.basename(image_path))[0] + '.txt'
    output_file = os.path.join(output_folder, filename)

    # Write the biographies to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        for bio in biographies:
            f.write(bio)
            f.write('\n')
            f.write('-' * 80)
            f.write('\n')

    print(f'Biographies saved to: {output_file}')


extract_biographies_to_file('data/raw-images/0254.1.tif')

