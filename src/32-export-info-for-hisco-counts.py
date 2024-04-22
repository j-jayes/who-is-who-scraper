import pandas as pd
import os
import json
from pathlib import Path

# Define the base directory
base_directory = "data/json_structured_geocoded_hisco"

# Prepare a list to collect all individual occupation data
individuals = []

# Loop through the files to collect occupation data for each individual
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
                                person_id = key
                                full_name = person_data.get('full_name', '')
                                occupation = person_data.get('occupation', '')
                                hisco_code = person_data.get('occupation_hisco_code', '')
                                hisco_occupation = person_data.get('occupation_hisco_occupation', '')
                                occupation_cosine_similarity = person_data.get('occupation_cosine_similarity', 0)


                                # Initialize current location variables
                                current_lon = ''
                                current_lat = ''

                                location_coordinates = person_data.get('location_coordinates', {})

                                if location_coordinates:
                                    current_lat = location_coordinates.get('Latitude', None)
                                    current_lon = location_coordinates.get('Longitude', None)

                                birth_details = person_data.get('birth_details', {})

                                # Initialize birth variables
                                birth_date = ''
                                birth_place = ''
                                birth_lat = ''
                                birth_lon = ''
                                parents = ''

                                if birth_details:
                                    birth_date = birth_details.get('date', '')
                                    birth_place = birth_details.get('place', '')
                                    parents = birth_details.get('parents', [])
                                    coordinates = birth_details.get('place_coordinates', {})
                                    if coordinates:
                                        birth_lat = coordinates.get('Latitude', '')
                                        birth_lon = coordinates.get('Longitude', '')

                                # Initialize education variables
                                degree = 'None'
                                institution = 'None'
                                
                                # Retrieve and handle education data
                                education_data = person_data.get('education', None)
                                if education_data:
                                    if isinstance(education_data, list) and education_data:
                                        # Access the last element if education_data is a list
                                        last_education = education_data[-1]
                                    elif isinstance(education_data, dict):
                                        # Directly use the dictionary if education_data is a dictionary
                                        last_education = education_data
                                    else:
                                        last_education = None

                                    if last_education:
                                        degree = last_education.get('degree', 'None')
                                        institution = last_education.get('institution', '')
                                
                                # Collect individual data
                                if hisco_code and isinstance(hisco_occupation, str):
                                    individuals.append({
                                        'person_id': person_id,
                                        'full_name': full_name,
                                        'occupation': occupation,
                                        'hisco_code': hisco_code,
                                        'hisco_occupation': hisco_occupation,
                                        'occupation_cosine_similarity': occupation_cosine_similarity,
                                        'current_lat': current_lat,
                                        'current_lon': current_lon,
                                        'degree': degree,
                                        'institution': institution,
                                        'birth_date': birth_date,
                                        'birth_place': birth_place,
                                        'birth_lat': birth_lat,
                                        'birth_lon': birth_lon,
                                        'parents': parents
                                    })

# Convert list of dictionaries to a DataFrame
df = pd.DataFrame(individuals)

# Save the DataFrame to an Excel file
output_excel_path = 'data/occupations/individual_occupations.xlsx'
Path(os.path.dirname(output_excel_path)).mkdir(parents=True, exist_ok=True)
df.to_excel(output_excel_path, index=False)

print("Data saved to Excel successfully!")
