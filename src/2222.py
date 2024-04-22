import os
import json
from collections import Counter

base_directory = "data/json_structured_geocoded_hisco_sector"

hisco_codes_of_interest = [20, 21, 22, 23, 24, 25, 27, 28, 29]
sector_counter = Counter()
individuals_count = 0

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

                        # Load the biography file
                        with open(file_path, 'r') as file:
                            bio_data = json.load(file)

                        # Check if 'structured' key exists
                        if 'structured' in bio_data:
                            for entry in bio_data['structured'].values():
                                # Check HISCO code
                                hisco_code = entry.get('occupation_hisco_code')
                                if hisco_code in hisco_codes_of_interest:
                                    individuals_count += 1
                                    sector = entry.get('sector_description', 'Unknown')
                                    sector_counter[sector] += 1

# Results
print(f"Total individuals with HISCO code 20 or 22: {individuals_count}")
print("Sector count for these individuals:")
for sector, count in sector_counter.items():
    print(f"  {sector}: {count}")



import os
import json
from collections import Counter

base_directory = "data/json_structured_geocoded_hisco_sector"

hisco_codes_of_interest = [211]
sector_counter = Counter()
individuals_count = 0

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

                        # Load the biography file
                        with open(file_path, 'r') as file:
                            bio_data = json.load(file)

                        # Check if 'structured' key exists
                        if 'structured' in bio_data:
                            for entry in bio_data['structured'].values():
                                # Check HISCO code
                                hisco_code = entry.get('occupation_hisco_code')
                                if hisco_code in hisco_codes_of_interest:
                                    individuals_count += 1
                                    sector = entry.get('sector_description', 'Unknown')
                                    sector_counter[sector] += 1

# Results
print(f"Total individuals with HISCO code 20 or 22: {individuals_count}")
print("Sector count for these individuals:")
for sector, count in sector_counter.items():
    print(f"  {sector}: {count}")
