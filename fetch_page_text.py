import requests
import time
from bs4 import BeautifulSoup

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

# 1061 

# http://runeberg.org/vemarvem/gota48/1074.html

for i in range(20, 1074):
    url = f"http://runeberg.org/vemarvem/gota48/{str(i).zfill(4)}.html"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract the text using the extract_bio_data function
        bio_data = extract_bio_data(str(soup))

        if bio_data:
            with open(f"data/raw/gota_48_page_text_{i}.txt", "w", encoding="UTF-8") as f:
                f.write(bio_data)
            print(f"Text has been saved to gota_48_page_text_{i}.txt")

        else:
            print(f"Biographical data not found for page {i}.")

        # Wait for a respectful amount of time before making the next request
        time.sleep(10)

    else:
        print(f"Failed to fetch page {i}. Status code: {response.status_code}")
