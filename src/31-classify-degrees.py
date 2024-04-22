"""
What do I want to do?

I want to collect the different degrees in order to classify them.

"""

import json
import os
from collections import Counter
from pathlib import Path
import re

def extract_degrees(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

    degrees = []
    for key, person_data in data.get('structured', {}).items():
        if isinstance(person_data, dict):
            # Extract education institutions
            education = person_data.get('education', [])
            if education:
                education_places = [edu.get('degree', '') for edu in education if isinstance(edu, dict) and isinstance(edu.get('institution', ''), str)]
                degrees.extend(filter(None, education_places))

    return degrees

def create_degrees_cache(base_dir, cache_file):
    degrees_counter = Counter()

    for book_name in os.listdir(base_dir):
        book_path = os.path.join(base_dir, book_name)
        if os.path.isdir(book_path):
            for letter in os.listdir(book_path):
                letter_path = os.path.join(book_path, letter)
                if os.path.isdir(letter_path):
                    for filename in os.listdir(letter_path):
                        if filename.endswith(".json"):
                            file_path = os.path.join(letter_path, filename)
                            degrees = extract_degrees(file_path)
                            for location in degrees:
                                degrees_counter.update([location])  # Update with individual location

    # Save degrees and counts to cache file
    Path(os.path.dirname(cache_file)).mkdir(parents=True, exist_ok=True)
    with open(cache_file, "w") as outfile:
        json.dump(dict(degrees_counter), outfile, indent=4, ensure_ascii=False)

# Define the base directory and cache file path
base_directory = "data/json_structured"
cache_file_path = "data/degrees/degrees_cache.json"

# ensure cache directory exists
Path(os.path.dirname(cache_file_path)).mkdir(parents=True, exist_ok=True)

# Create the degrees cache
create_degrees_cache(base_directory, cache_file_path)

# read in the degrees cache
with open(cache_file_path, "r") as file:
    data = json.load(file)

# arrange the degrees in descending order of count
sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))

# save the sorted data to an excel file
import pandas as pd
import shutil

df = pd.DataFrame(sorted_data.items(), columns=['Degree', 'Count'])
df.to_excel("data/degrees/degrees.xlsx", index=False)

degrees_df = pd.read_excel("data/degrees/degrees.xlsx")

def modify_patterns_for_broader_matching(fields):
    modified_fields = {}
    for field, patterns in fields.items():
        modified_patterns = []
        for pattern in patterns:
            if len(pattern) >= 4:  # Modify patterns that are 4 characters or longer
                # Remove word boundary assertions (\b) if they exist
                pattern = re.sub(r'\\b', '', pattern)
            modified_patterns.append(pattern)
        modified_fields[field] = modified_patterns
    return modified_fields

# Update the fields dictionary with broader pattern matching
updated_fields = modify_patterns_for_broader_matching({
    'General Education': ['Stud', 'Studentexamen', 'Realexamen', 'Folkskollärarexamen', 'Mogenhetsexamen', 'Studexamen', 'Studenterexamen', 'Studentersexamen', 'Studiexamen', 'Studrex', 'Studiex', 'Stud:-ex.', 'Mogenhetsexamen', 'Stud:ex'],
    'Philosophy and Theology': ['Filosofie', 'Teologisk', 'Teologie', 'fil', 'teol kand', 'teol. kand.', 'Teologie kandidat', 'Teologisk filosofiexamen', 'teol. fil. ex.', 'fil kand'],
    'Medical Sciences': [
        'Medicine', 'medicinsk', 'Tandläkarexamen', 'tandläkare', 'tandl', 
        'Apotekarexamen', 'apot', 'Veterinärexamen', 'vet', 'med kand', 'med lic', 'Med. kand.', 'Med. lic.', 'tandl:ex', 'Tandl:ex', 'Medicinsk licentiat', 'Medicinsk kandidat', 'medicinsk licentiat', 'medicinsk kandidat', 'Medicinsk licentiat', 'Medicinsk kandidat'
    ],
    'Law and Social Sciences': ['Juris', 'jur', 'Juristexamen', 'Juridik', 'jur kand', 'jur. kand.', 'Jur.kand.', 'Juristexamen'],
    'Engineering and Technical': ['Civilingenjör', 'Ingenjörsexamen', 'Ingenjör', 'CTH', 'KTH', 'ing', 'tekn', 'Ing:ex', 'ingenjörsexamen', 'ing:ex', 'ingenjör', 'Civilingenjörsexamen'],
    'Business and Commerce': ['handel', 'ekonomi', 'hdl', 'Hdlsgymn', 'Hbgs hdlsgymn', 'Handelshögskola', 'Handelsgymnasium'],
    'Public Administration and Civil Service': ['kansli', 'admin', 'civ', 'Kansliex', 'Civilekonom'],
    'Military': ['Kapten', 'Major', 'Sjökaptensexamen', 'officersexamen', 'reservofficersexamen', 'Reservofficersexamen', 'Officersexamen', 'Off:ex'],
    'Higher Academia and Research': ['doktor', 'lic', 'dr', 'forsk', 'fil dr', 'Docent', 'Professor', 'docent', 'professor', 'Filosofie doktor'],
    'Educational Institutions': ['Folkhögskola', 'Folkhögsk'],
    'Agricultural and Environmental Sciences': ['Agronomexamen', 'Lantmästarexamen']
})

# Redefine the classification function with the updated fields
def classify_degree_field_and_level_final(degree):
    fields = updated_fields
    levels = {
        'Candidate': ['kand', 'kandidat', 'Kandidat', 'med kand'],
        'Licentiate': ['lic', 'licentiat', 'med lic'],
        'Doctor': ['dr', 'doktor', 'Doctor', 'Doktor'],
        'Bachelor': ['bachelor', 'grundexamen'],
        'Master': ['magister', 'master', 'måg', 'mag']
    }

    if not isinstance(degree, str):
        return 'Miscellaneous', 'N/A'

    field_category = 'Miscellaneous'
    for field, patterns in fields.items():
        if any(re.search(pattern, degree, re.IGNORECASE) for pattern in patterns):
            field_category = field
            break

    level_category = 'N/A'
    for level, patterns in levels.items():
        if any(re.search(pattern, degree, re.IGNORECASE) for pattern in patterns):
            level_category = level
            break

    return field_category, level_category

# Apply the final refined classification function
degrees_df['degree_group'], degrees_df['degree_level'] = zip(*degrees_df['Degree'].apply(classify_degree_field_and_level_final))

# drop duplicates
degrees_df.drop_duplicates(subset=['Degree'], keep='first', inplace=True)

# to excel file in "data/degrees/degrees_classified.xlsx"
degrees_df.to_excel("data/degrees/degrees_classified.xlsx", index=False)

######### Mapping degrees to classification and level #########

# First copy "data/json_structured_geocoded_hisco_sector" and all its contents to "data/json_structured_geocoded_hisco_sector_degrees"

# copy "data/json_structured_geocoded_hisco_sector" and all its contents to "data/json_structured_geocoded_hisco_sector_degrees"
import shutil
shutil.copytree("data/json_structured_geocoded_hisco_sector", "data/json_structured_geocoded_hisco_sector_degrees")


# Load the mapping directly from the prepared dictionary (for the purpose of this example, assume it's loaded here)
degree_mapping = {
    degree_row['Degree']: {
        'classification': degree_row['degree_group'],
        'level': degree_row['degree_level']
    } for _, degree_row in degrees_df.iterrows() if pd.notna(degree_row['degree_group']) and pd.notna(degree_row['degree_level'])
}

# Function to add degree classification and level
def add_degree_info(edu_entry):
    degree_name = edu_entry['degree']
    if degree_name in degree_mapping:
        edu_entry['classification'] = degree_mapping[degree_name]['classification']
        edu_entry['level'] = degree_mapping[degree_name]['level']

# Define the base directory
base_directory = "data/json_structured_geocoded_hisco_sector_degrees"
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
                                    # Add coordinates and degree info to each 'education' -> 'institution'
                                    if 'education' in entry and isinstance(entry['education'], list):
                                        for edu in entry['education']:
                                            if 'degree' in edu and isinstance(edu['degree'], str):
                                                add_degree_info(edu)

                            # Save the updated biography data
                            with open(file_path, 'w') as file:
                                json.dump(bio_data, file, indent=4, ensure_ascii=False)

                        except Exception as e:
                            print(f"An error occurred while processing {file_path}: {e}. Skipping this file.")

