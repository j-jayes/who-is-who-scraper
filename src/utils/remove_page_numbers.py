import os
import re


def remove_page_number(file_path, page_number):
    """
    Removes a number from the end of a text file if the number is within 50 of the specified page_number.

    Args:
        file_path (str): The path to the text file.
        page_number (int): The reference page number.

    Returns:
        None

    Raises:
        None

    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Reverse the lines to start from the bottom
    lines_reversed = lines[::-1]

    # Define the range for acceptable numbers to remove
    lower_bound = page_number - 50
    upper_bound = page_number + 50

    # Find the last non-empty line
    for index, line in enumerate(lines_reversed):
        stripped_line = line.strip()
        if stripped_line:
            try:
                # Convert the line to an integer for comparison
                line_number = int(stripped_line)
                if lower_bound <= line_number <= upper_bound:
                    # If the line number is within the defined range, remove the line
                    del lines[-(index + 1)]
                    break
                else:
                    # If not in range, exit the loop without doing anything
                    break
            except ValueError:
                # If the line cannot be converted to an integer, just break
                break

    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

def main():
    directory = 'data/raw/'

    # Regular expression to match the filenames
    pattern = re.compile(r'^(skane48|sthlm62|sthlm45|svea64|gota48|gota65|skane66|norr68)_page_text_(\d{1,4})\.txt$')

    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        match = pattern.match(filename)
        
        # If the filename matches the pattern
        if match:
            book, page_number = match.groups()
            page_number = int(page_number)

            file_path = os.path.join(directory, filename)

            if os.path.isfile(file_path):
                remove_page_number(file_path, page_number)
            else:
                print(f"File not found: {file_path}")
        else:
            print(f"Filename format not recognized: {filename}")

if __name__ == '__main__':
    main()
