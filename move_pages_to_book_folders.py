import os
import shutil
import json

# Example usage
with open("data/number_of_pages_per_book.json", "r") as infile:
    number_of_pages_per_book = json.load(infile)

data_raw_path = "data/raw"


# Create subfolders for each book
for book_id, num_pages in number_of_pages_per_book.items():
    book_folder_name = f"{book_id}"
    book_folder_path = os.path.join(data_raw_path, book_folder_name)
    
    if not os.path.exists(book_folder_path):
        os.makedirs(book_folder_path)

# Move the text files into their respective subfolders
for file_name in os.listdir(data_raw_path):
    if file_name.endswith(".txt"):
        book_id = file_name.split('_')[0]
        year = book_id[-2:]  # Extract the year from the book_id
        book_folder_name = f"{book_id}_{year}"
        
        src_file_path = os.path.join(data_raw_path, file_name)
        dest_file_path = os.path.join(data_raw_path, book_folder_name, file_name)
        
        shutil.move(src_file_path, dest_file_path)
        print(f"Moved {src_file_path} to {dest_file_path}")