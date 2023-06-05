import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


url = "http://runeberg.org/vemarvem/sthlm45/"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")

    letter_heading = soup.find('h2', text=re.compile('^A'))

    if letter_heading is not None:
        # Find all the <a> tags that are siblings of the <br> tag immediately following the letter heading
        br_tag = letter_heading.find_next_sibling('br')
        if br_tag is not None:
            page_links = br_tag.find_next_siblings('a')
        else:
            page_links = []
    else:
        page_links = []

    # Group the page links by letter name
    letters = {}
    for link in page_links:
        letter_name = link.previous_sibling.strip()
        if letter_name not in letters:
            letters[letter_name] = []
        letters[letter_name].append(link['href'])

    # Print the result
    for letter, pages in letters.items():
        print(f"{letter}: {', '.join(pages)}")

    # Create pandas dataframe from dictionary
    df = pd.DataFrame(letters.items(), columns=['Letter', 'Pages'])

    # Save dataframe to CSV file
    df.to_csv('book_table_of_contents.csv', index=False)

    # Print the result
    print(df)

else:
    print("Error accessing website")
