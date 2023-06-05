import os
import json
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

def geocode_birthplace(birthplace, geolocator, geocoded_cache):
    if isinstance(birthplace, dict):
        if "name" in birthplace:
            birthplace_name = birthplace["name"]
        elif "address" in birthplace and "addressLocality" in birthplace["address"]:
            birthplace_name = birthplace["address"]["addressLocality"]
        else:
            print(f"Invalid birthplace data: {birthplace}")
            return None
    elif isinstance(birthplace, str):
        birthplace_name = birthplace
    else:
        print(f"Invalid birthplace data: {birthplace}")
        return None

    if birthplace_name not in geocoded_cache:
        try:
            location = geolocator.geocode(birthplace_name)
            if location:
                geocoded_cache[birthplace_name] = {
                    "latitude": location.latitude,
                    "longitude": location.longitude
                }
            time.sleep(1)  # Add a 1-second delay between geocoding requests
        except Exception as e:
            print(f"Error geocoding birthplace {birthplace_name}: {e}")

    return geocoded_cache.get(birthplace_name)



def augment_biography(input_directory, output_directory, file_name, geolocator, geocoded_cache):
    try:
        input_file_path = os.path.join(input_directory, file_name)
        output_file_path = os.path.join(output_directory, file_name)

        with open(input_file_path, "r", encoding="utf-8") as input_file:
            data = json.load(input_file)

        structured_biography = data["structured"]

        if "birthPlace" in structured_biography:
            birthplace = structured_biography["birthPlace"]
            geocoded_birthplace = geocode_birthplace(birthplace, geolocator, geocoded_cache)

            if geocoded_birthplace:
                if isinstance(birthplace, dict):
                    structured_biography["birthPlace"]["latitude"] = geocoded_birthplace["latitude"]
                    structured_biography["birthPlace"]["longitude"] = geocoded_birthplace["longitude"]
                else:
                    structured_biography["birthPlace"] = {
                        "name": birthplace,
                        "latitude": geocoded_birthplace["latitude"],
                        "longitude": geocoded_birthplace["longitude"]
                    }

        with open(output_file_path, "w", encoding="utf-8") as output_file:
            json.dump(data, output_file, ensure_ascii=False, indent=4)

        print(f"Processed file: {file_name}")

    except Exception as e:
        print(f"Error processing file {file_name}: {e}")


def main():
    input_directory = "data/biographies_translated"
    output_directory = "data/biographies_augmented"
    locations_directory = "data/locations"
    os.makedirs(output_directory, exist_ok=True)
    os.makedirs(locations_directory, exist_ok=True)

    locations_file = os.path.join(locations_directory, "geocoded_locations.json")

    # Load the geocoded locations from the JSON file
    if os.path.exists(locations_file):
        with open(locations_file, "r", encoding="utf-8") as f:
            geocoded_cache = json.load(f)
    else:
        geocoded_cache = {}

    geolocator = Nominatim(user_agent="myGeocoder")

    all_files = sorted([f for f in os.listdir(input_directory) if f.endswith(".json")])

    # Process only the first 10 files
    for file_name in all_files:
        augment_biography(input_directory, output_directory, file_name, geolocator, geocoded_cache)

    # Save the updated geocoded locations to the JSON file
    with open(locations_file, "w", encoding="utf-8") as f:
        json.dump(geocoded_cache, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
