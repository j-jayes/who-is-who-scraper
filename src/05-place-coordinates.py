import json
import os
from pathlib import Path

# Restructure the JSON object to be a single JSON array
def restructure_json(input_file, output_file):
    try:
        with open(input_file, 'r') as file:
            # Read all lines and parse each line as a JSON object
            data = [json.loads(line) for line in file]

        with open(output_file, 'w') as file:
            # Write the data as a single JSON array
            json.dump(data, file, indent=4, ensure_ascii=False)

        print(f"File '{output_file}' has been created with the restructured JSON.")

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


restructure_json('data/locations/geocoded_locations.json', 'data/locations/geocoded_locations_restructured.json')

import json
import os

# Load the locations file
with open('data/locations/geocoded_locations_restructured.json', 'r') as file:
    locations_data = json.load(file)

# Creating a dictionary for location lookup
location_lookup = {list(location.keys())[0]: list(location.values())[0] for location in locations_data}

# Function to add coordinates to a field if the location exists in the lookup
def add_coordinates(entry, field_name):
    if field_name in entry and isinstance(entry[field_name], str) and entry[field_name] in location_lookup:
        entry[field_name + '_coordinates'] = location_lookup[entry[field_name]]

# Define the base directory
base_directory = "data/json_structured_geocoded"
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

                        try:
                            # Load the biography file
                            with open(file_path, 'r') as file:
                                bio_data = json.load(file)

                            # Check if 'structured' key exists and is a dictionary with values
                            if 'structured' in bio_data and isinstance(bio_data['structured'], dict) and bio_data['structured']:
                                # Iterate through each biography entry
                                for entry in bio_data['structured'].values():
                                    # Add coordinates to 'location'
                                    add_coordinates(entry, 'location')

                                    # Add coordinates to 'birth_details' -> 'place'
                                    if 'birth_details' in entry and isinstance(entry['birth_details'], dict) and 'place' in entry['birth_details'] and isinstance(entry['birth_details']['place'], str):
                                        place = entry['birth_details']['place']
                                        if place in location_lookup:
                                            entry['birth_details']['place_coordinates'] = location_lookup[place]

                                    # Add coordinates to each 'education' -> 'institution'
                                    if 'education' in entry and isinstance(entry['education'], list):
                                        for edu in entry['education']:
                                            if 'institution' in edu and isinstance(edu['institution'], str) and edu['institution'] in location_lookup:
                                                edu['institution_coordinates'] = location_lookup[edu['institution']]

                            # Save the updated biography data
                            with open(file_path, 'w') as file:
                                json.dump(bio_data, file, indent=4, ensure_ascii=False)

                        except Exception as e:
                            print(f"An error occurred while processing {file_path}: {e}. Skipping this file.")