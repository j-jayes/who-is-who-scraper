import pandas as pd
import json
import os
from pathlib import Path

hisco_mapping = pd.read_json('data/occupations/closest_hisco_matches.json')

# replace wherever the hisco occupation is "Draughtsmen", change it to "General Managers" and set the hisco code to 211
hisco_mapping.loc[hisco_mapping['hisco_occupation'] == 'Draughtsmen', 'hisco_code'] = 211
hisco_mapping.loc[hisco_mapping['hisco_occupation'] == 'Draughtsmen', 'hisco_occupation'] = 'General Managers'


# define a function to add the hisco code to the biography data along with the cosine similarity and hisco_occupation
def add_hisco_code(entry, field_name):
    if field_name in entry and isinstance(entry[field_name], str) and entry[field_name] in hisco_mapping['occupation'].to_list():
        hisco_row = hisco_mapping[hisco_mapping['occupation'] == entry[field_name]]
        # convert the hisco to an integer
        entry[field_name + '_hisco_code'] = int(hisco_row['hisco_code'].values[0])
        # convert the cosine similarity to a float
        entry[field_name + '_cosine_similarity'] = float(hisco_row['cosine_similarity'].values[0])
        entry[field_name + '_hisco_occupation'] = hisco_row['hisco_occupation'].values[0]

# Define the base directory
base_directory = "data/json_structured_geocoded"

# define the new output directory
output_directory = "data/json_structured_geocoded_hisco"

# Traverse the nested directories
for book_name in os.listdir(base_directory):
    book_path = os.path.join(base_directory, book_name)
    if os.path.isdir(book_path):
        for letter in os.listdir(book_path):
            letter_path = os.path.join(book_path, letter)
            if os.path.isdir(letter_path):
                for filename in os.listdir(letter_path):
                    if filename.endswith(".json"):
                        file_path = os.path.join(letter_path, filename)
                        # create the output directory if it doesn't exist
                        Path(os.path.dirname(file_path.replace(base_directory, output_directory))).mkdir(parents=True, exist_ok=True)
                        # set the output filename
                        output_file_path = file_path.replace(base_directory, output_directory)

                        try:
                            # Load the biography file
                            with open(file_path, 'r') as file:
                                bio_data = json.load(file)

                            # Check if 'structured' key exists and is a dictionary with values
                            if 'structured' in bio_data and isinstance(bio_data['structured'], dict) and bio_data['structured']:
                                # Iterate through each biography entry
                                for entry in bio_data['structured'].values():
                                    # Add hisco code to 'occupation'
                                    add_hisco_code(entry, 'occupation')

                            # Save the updated biography data
                            with open(output_file_path, 'w') as file:
                                json.dump(bio_data, file, indent=4, ensure_ascii=False)

                        except Exception as e:
                            print(f"An error occurred while processing {file_path}: {e}. Skipping this file.")