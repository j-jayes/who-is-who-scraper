import requests
import time
from bs4 import BeautifulSoup
import json

resume_book_id = "skane66"
resume_page = 345

def extract_bio_data(page_source):
    start_tag = "<!-- mode=normal -->"
    end_tag = "<!-- NEWIMAGE2 -->"

    start_index = page_source.find(start_tag)
    end_index = page_source.find(end_tag)

    if start_index == -1 or end_index == -1:
        return None

    start_index += len(start_tag)
    bio_data = page_source[start_index:end_index].strip()

    return bio_data

def fetch_book_text(book_id, num_pages, start_page=1):
    for i in range(start_page, num_pages + 1):
        # (Rest of the code remains the same)
        url = f"http://runeberg.org/vemarvem/{book_id}/{str(i).zfill(4)}.html"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract the text using the extract_bio_data function
            bio_data = extract_bio_data(str(soup))

            if bio_data:
                with open(f"data/raw/{book_id}_page_text_{i}.txt", "w", encoding="UTF-8") as f:
                    f.write(bio_data)
                print(f"Text has been saved to {book_id}_page_text_{i}.txt")

            else:
                print(f"Biographical data not found for page {i}.")

            # Wait for a respectful amount of time before making the next request
            time.sleep(5)

        else:
            print(f"Failed to fetch page {i}. Status code: {response.status_code}")

# Example usage
with open("data/number_of_pages_per_book.json", "r") as infile:
    number_of_pages_per_book = json.load(infile)

# Update the loop like this:
found_resume_book = False
for book_id, num_pages in number_of_pages_per_book.items():
    if not found_resume_book:
        if book_id == resume_book_id:
            found_resume_book = True
            print(f"Resuming text fetching for {book_id}...")
            fetch_book_text(book_id, num_pages, resume_page)
        else:
            print(f"Skipping {book_id}...")
            continue
    else:
        print(f"Fetching text for {book_id}...")
        fetch_book_text(book_id, num_pages)