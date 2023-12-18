import os

def remove_page_number(file_path, page_number):
    """
    Removes the specified page number from the end of a text file.

    Args:
        file_path (str): The path to the text file.
        page_number (int): The page number to be removed.

    Returns:
        None

    Raises:
        None

    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Reverse the lines to start from the bottom
    lines_reversed = lines[::-1]

    # Find the last non-empty line
    for index, line in enumerate(lines_reversed):
        if line.strip():
            if line.strip() == str(page_number):
                # Remove the page number line
                del lines[-(index + 1)]
                break
            else:
                # No page number found, exit the loop
                break

    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

def main():
    directory = 'data/raw'

    for number in range(17, 1074):
        file_name = f'gota48_page_text_{number}.txt'
        file_path = os.path.join(directory, file_name)

        if os.path.isfile(file_path):
            remove_page_number(file_path, number)
        else:
            print(f"File not found: {file_path}")

if __name__ == '__main__':
    main()
