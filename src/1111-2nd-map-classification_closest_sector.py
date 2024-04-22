import pandas as pd
import json
import os
from pathlib import Path

hisco_mapping = pd.read_json('data/careers/closest_sector_matches.json')


hisco_mapping.columns

# rename hisco_code to sector in hisco_mapping
hisco_mapping.rename(columns={'hisco_code': 'sector_code'}, inplace=True)
# rename hisco_occupation to sector_description in hisco_mapping
hisco_mapping.rename(columns={'hisco_occupation': 'sector_description'}, inplace=True)

cache_file = 'data/careers/last_careers_cache.json'

last_careers = pd.read_json(cache_file)

last_careers.columns

# join hisco_mapping to last_careers on career_info = occupation
last_careers_map = last_careers.merge(hisco_mapping, how='left', left_on='career_info', right_on='occupation')

#convert last_careers_map to a dictionary
last_careers_map_dict = last_careers_map.to_dict(orient='records')

# set dictionary index to career_info
last_careers_map_dict = {d['career_info']: d for d in last_careers_map_dict}



import json
import os

# Define the base directory
base_directory = "data/json_structured_geocoded_hisco"

# define the new output directory
output_directory = "data/json_structured_geocoded_hisco_sector"
# ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

def update_sector_info(entry, careers_map_dict):
    if 'career' in entry and isinstance(entry['career'], list) and entry['career']:
        last_career_entry = entry['career'][-1]
        position = last_career_entry.get('position', '')
        organization = last_career_entry.get('organization', '')

        # Concatenate position and organization for the lookup
        career_info = f"{position} {organization}".strip()

        # Find the sector info in the map using career_info
        sector_info = careers_map_dict.get(career_info)
        if sector_info:
            entry['sector_code'] = sector_info.get('sector_code')
            entry['sector_description'] = sector_info.get('sector_description')




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
                        # Create the output directory if it doesn't exist
                        Path(os.path.dirname(file_path.replace(base_directory, output_directory))).mkdir(parents=True, exist_ok=True)
                        # Set the output filename
                        output_file_path = file_path.replace(base_directory, output_directory)

                        try:
                            # Load the biography file
                            with open(file_path, 'r') as file:
                                bio_data = json.load(file)

                            # Check if 'structured' key exists and is a dictionary with values
                            if 'structured' in bio_data and isinstance(bio_data['structured'], dict) and bio_data['structured']:
                                # Iterate through each biography entry
                                for entry in bio_data['structured'].values():
                                    # Update entry with sector info
                                    update_sector_info(entry, last_careers_map_dict)

                            # Save the updated biography data
                            with open(output_file_path, 'w') as file:
                                json.dump(bio_data, file, indent=4, ensure_ascii=False)

                        except Exception as e:
                            print(f"An error occurred while processing {file_path}: {e}. Skipping this file.")