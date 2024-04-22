import pandas as pd
import os
import json
from pathlib import Path
from collections import Counter


# This file will count the most common hisco codes. 

# define the base directory
base_directory = "data/json_structured_geocoded_hisco"

# define the output file
output_file = "data/occupations/hisco_counts.json"

# loop through the files and count occupation_hisco_code 
hisco_counts = Counter()

for book_name in os.listdir(base_directory):
    book_path = os.path.join(base_directory, book_name)
    if os.path.isdir(book_path):
        for letter in os.listdir(book_path):
            letter_path = os.path.join(book_path, letter)
            if os.path.isdir(letter_path):
                for filename in os.listdir(letter_path):
                    if filename.endswith(".json"):
                        file_path = os.path.join(letter_path, filename)
                        with open(file_path, "r") as file:
                            data = json.load(file)
                        for key, person_data in data.get('structured', {}).items():
                            if isinstance(person_data, dict):
                                # Extract occupation_hisco_code and occupation_hisco_occupation
                                current_occupation= person_data.get('occupation_hisco_occupation', '')
                                if current_occupation and isinstance(current_occupation, str):
                                    hisco_counts.update([current_occupation])



# save the hisco counts to a json file
Path(os.path.dirname(output_file)).mkdir(parents=True, exist_ok=True)
with open(output_file, "w") as outfile:
    json.dump(dict(hisco_counts), outfile, indent=4, ensure_ascii=False)

# arrange hisco counts
hisco_counts_df = pd.DataFrame.from_dict(hisco_counts, orient='index', columns=['count'])
hisco_counts_df = hisco_counts_df.sort_values(by=['count'], ascending=False)

# save to excel at data/occupations/hisco_counts_ordered.xlsx
hisco_counts_df.to_excel('data/occupations/hisco_counts_ordered.xlsx')




# This section will extract the birthplace

# define the output file
output_file = "data/occupations/hisco_counts.json"

# loop through the files and count occupation_hisco_code 
hisco_counts = Counter()

for book_name in os.listdir(base_directory):
    book_path = os.path.join(base_directory, book_name)
    if os.path.isdir(book_path):
        for letter in os.listdir(book_path):
            letter_path = os.path.join(book_path, letter)
            if os.path.isdir(letter_path):
                for filename in os.listdir(letter_path):
                    if filename.endswith(".json"):
                        file_path = os.path.join(letter_path, filename)
                        with open(file_path, "r") as file:
                            data = json.load(file)
                        for key, person_data in data.get('structured', {}).items():
                            if isinstance(person_data, dict):
                                # Extract occupation_hisco_code and occupation_hisco_occupation
                                current_occupation= person_data.get('occupation_hisco_occupation', '')
                                if current_occupation and isinstance(current_occupation, str):
                                    hisco_counts.update([current_occupation])



# save the hisco counts to a json file
Path(os.path.dirname(output_file)).mkdir(parents=True, exist_ok=True)
with open(output_file, "w") as outfile:
    json.dump(dict(hisco_counts), outfile, indent=4, ensure_ascii=False)

# arrange hisco counts
hisco_counts_df = pd.DataFrame.from_dict(hisco_counts, orient='index', columns=['count'])
hisco_counts_df = hisco_counts_df.sort_values(by=['count'], ascending=False)

# save to excel at data/occupations/hisco_counts_ordered.xlsx
hisco_counts_df.to_excel('data/occupations/hisco_counts_ordered.xlsx')