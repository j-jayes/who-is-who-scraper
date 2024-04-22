from geopy.distance import geodesic
import json
import os
from collections import defaultdict

def calculate_distance(point1, point2):
    try:
        return geodesic((point1['Latitude'], point1['Longitude']), (point2['Latitude'], point2['Longitude'])).kilometers
    except:
        return None

base_directory = "data/json_structured_geocoded_hisco_sector"

hisco_codes_of_interest = [221]
sector_distances = defaultdict(list)

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
                            with open(file_path, 'r') as file:
                                bio_data = json.load(file)

                            for person_id, person in bio_data.get('structured', {}).items():
                                hisco_code = person.get('occupation_hisco_code')
                                if hisco_code in hisco_codes_of_interest:
                                    birth_coords = person['birth_details'].get('place_coordinates')
                                    current_coords = person.get('location_coordinates')
                                    education_coords = person['education'][0].get('institution_coordinates') if person['education'] else None
                                    sector = person.get('sector_description', 'Unknown')

                                    distances = []
                                    if birth_coords and education_coords:
                                        distance = calculate_distance(birth_coords, education_coords)
                                        if distance is not None:
                                            distances.append(distance)

                                    if birth_coords and current_coords:
                                        distance = calculate_distance(birth_coords, current_coords)
                                        if distance is not None:
                                            distances.append(distance)

                                    if distances:
                                        sector_distances[sector].append(sum(distances) / len(distances))

                        except Exception as e:
                            print(f"Error processing file {file_path}: {e}")

# Calculate the average distance for each sector
average_distances_by_sector = {sector: sum(distances)/len(distances) for sector, distances in sector_distances.items() if distances}

# Print results
for sector, avg_distance in average_distances_by_sector.items():
    print(f"Sector: {sector}, Average Distance: {avg_distance:.2f} km")
