import requests
from bs4 import BeautifulSoup
import json


def find_number_of_pages(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('a', href=True)

    max_page_number = 0
    for link in links:
        href = link['href']
        if href.endswith('.html') and href[:-5].isdigit():
            page_number = int(href[:-5])
            max_page_number = max(max_page_number, page_number)

    return max_page_number

url = "http://runeberg.org/vemarvem/skane48/"
print(find_number_of_pages(url))


# Assuming find_number_of_pages function is defined

urls = [
    "http://runeberg.org/vemarvem/skane48/",
    "http://runeberg.org/vemarvem/sthlm62/",
    "http://runeberg.org/vemarvem/svea64/",
    "http://runeberg.org/vemarvem/gota65/",
    "http://runeberg.org/vemarvem/skane66/",
    "http://runeberg.org/vemarvem/norr68/"
]

number_of_pages_per_book = {}

for url in urls:
    number_of_pages = find_number_of_pages(url)
    book_id = url.split("/")[-2]  # Extracting the book identifier from the URL
    number_of_pages_per_book[book_id] = number_of_pages

# Save the dictionary to a file
with open("data/number_of_pages_per_book.json", "w") as outfile:
    json.dump(number_of_pages_per_book, outfile)
