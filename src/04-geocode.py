import json
import os
from collections import Counter
from pathlib import Path
import requests
from dotenv import load_dotenv

load_dotenv()

def extract_locations(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

    locations = []
    for key, person_data in data.get('structured', {}).items():
        if isinstance(person_data, dict):
            # Extract current location
            current_location = person_data.get('location', '')
            if current_location and isinstance(current_location, str):
                locations.append(current_location)

            # Extract birth place
            birth_details = person_data.get('birth_details')
            if birth_details and 'place' in birth_details and isinstance(birth_details['place'], str):
                locations.append(birth_details['place'])

            # Extract education institutions
            education = person_data.get('education', [])
            if education:
                education_places = [edu.get('institution', '') for edu in education if isinstance(edu, dict) and isinstance(edu.get('institution', ''), str)]
                locations.extend(filter(None, education_places))

    return locations



def create_locations_cache(base_dir, cache_file):
    locations_counter = Counter()

    for book_name in os.listdir(base_dir):
        book_path = os.path.join(base_dir, book_name)
        if os.path.isdir(book_path):
            for letter in os.listdir(book_path):
                letter_path = os.path.join(book_path, letter)
                if os.path.isdir(letter_path):
                    for filename in os.listdir(letter_path):
                        if filename.endswith(".json"):
                            file_path = os.path.join(letter_path, filename)
                            locations = extract_locations(file_path)
                            for location in locations:
                                locations_counter.update([location])  # Update with individual location

    # Save locations and counts to cache file
    Path(os.path.dirname(cache_file)).mkdir(parents=True, exist_ok=True)
    with open(cache_file, "w") as outfile:
        json.dump(dict(locations_counter), outfile, indent=4, ensure_ascii=False)

# Define the base directory and cache file path
base_directory = "data/json_structured"
cache_file_path = "data/locations/locations_cache.json"

# ensure cache directory exists
Path(os.path.dirname(cache_file_path)).mkdir(parents=True, exist_ok=True)

# Create the locations cache
create_locations_cache(base_directory, cache_file_path)

# Google Maps Geocoding API key from .env
api_key = os.getenv('GOOGLE_MAPS_API_KEY')

# Define the geocoding function and append ", Sweden" to the address
def geocode(address, api_key):
    address = address + ", Sweden"  # Append ", Sweden" to the address
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'address': address, 'key': api_key}
    response = requests.get(url, params=params)
    data = response.json()
    if data['status'] == 'OK':
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        print(f"Geocoded {address} as {lat}, {lng}")
        return lat, lng
    else:
        return None, None

geocoded_file_path = 'data/locations/geocoded_locations.json'

# Load locations from the cache file
with open(cache_file_path, 'r') as file:
    locations = json.load(file)

# Function to save a single geocoded location
def save_geocoded_location(location, lat, lng):
    with open(geocoded_file_path, 'a') as outfile:  # Open file in append mode
        json.dump({location: {'Latitude': lat, 'Longitude': lng}}, outfile, ensure_ascii=False)
        outfile.write("\n")  # Write a newline character for separating entries


# Geocode each location and save immediately
for location in locations.keys():
    lat, lng = geocode(location, api_key)
    if lat is not None and lng is not None:
        save_geocoded_location(location, lat, lng)









# Define the function to update the files with coordinates

def update_files_with_coordinates(input_dir, output_dir, geocoded_locations_file):
    # Load geocoded locations
    with open(geocoded_locations_file, 'r') as file:
        geocoded_locations = json.load(file)

    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            input_file_path = os.path.join(input_dir, filename)

            with open(input_file_path, 'r') as file:
                data = json.load(file)

            # Update each firm's data with coordinates
            for key, firm_data in data.items():
                if isinstance(firm_data, dict) and 'location' in firm_data:
                    location = firm_data['location']
                    coordinates = geocoded_locations.get(location, None)
                    firm_data['coordinates'] = coordinates

            # Save the updated data to the output directory
            output_file_path = os.path.join(output_dir, filename)
            with open(output_file_path, 'w') as outfile:
                json.dump(data, outfile, indent=4, ensure_ascii=False)

# Define the input and output directories and the geocoded locations file
input_directory = 'data/processed/svindkal_structured'
output_directory = 'data/processed/svindkal_geocoded'
geocoded_locations_file = 'data/locations/geocoded_locations.json'

# Create output directory if it doesn't exist
Path(output_directory).mkdir(parents=True, exist_ok=True)

# Update the files with coordinates
update_files_with_coordinates(input_directory, output_directory, geocoded_locations_file)
