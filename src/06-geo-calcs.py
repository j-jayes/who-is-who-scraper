import os
import json
from geopy.distance import geodesic
import statistics
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Function to calculate distance between two points using geodesic distance
def calculate_distance(point1, point2):
    try:
        return geodesic((point1['Latitude'], point1['Longitude']), (point2['Latitude'], point2['Longitude'])).kilometers
    except:
        return None

# Define the base directory
base_directory = "data/json_structured_geocoded"

# Initialize lists to store individual distances
distances_birth_to_education = []
distances_birth_to_current = []
distances_education_to_current = []

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
                                structured_data = bio_data['structured']

                                for person_id, person in structured_data.items():
                                    birth_coords = person['birth_details'].get('place_coordinates')
                                    current_coords = person.get('location_coordinates')
                                    education_coords = person['education'][0].get('institution_coordinates') if person['education'] else None

                                    if birth_coords and education_coords:
                                        distance_birth_to_education = calculate_distance(birth_coords, education_coords)
                                        if distance_birth_to_education is not None:
                                            distances_birth_to_education.append(distance_birth_to_education)

                                    if birth_coords and current_coords:
                                        distance_birth_to_current = calculate_distance(birth_coords, current_coords)
                                        if distance_birth_to_current is not None:
                                            distances_birth_to_current.append(distance_birth_to_current)

                                    if education_coords and current_coords:
                                        distance_education_to_current = calculate_distance(education_coords, current_coords)
                                        if distance_education_to_current is not None:
                                            distances_education_to_current.append(distance_education_to_current)
                        except Exception as e:
                            print(f"Error processing file {file_path}: {e}")

# Calculate the median distances
median_distance_birth_to_education = statistics.median(distances_birth_to_education) if distances_birth_to_education else None
median_distance_birth_to_current = statistics.median(distances_birth_to_current) if distances_birth_to_current else None
median_distance_education_to_current = statistics.median(distances_education_to_current) if distances_education_to_current else None

print(f"Median distance from birthplace to education institution: {median_distance_birth_to_education} km")
print(f"Median distance from birthplace to current location: {median_distance_birth_to_current} km")
print(f"Median distance from education institution to current location: {median_distance_education_to_current} km")



# Initialize variables to store total distances and counts
total_distance_birth_to_education = 0
total_distance_birth_to_current = 0
total_distance_education_to_current = 0
count_birth_to_education = 0
count_birth_to_current = 0
count_education_to_current = 0

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
                                structured_data = bio_data['structured']

                                for person_id, person in structured_data.items():
                                    birth_coords = person['birth_details'].get('place_coordinates')
                                    current_coords = person.get('location_coordinates')
                                    education_coords = person['education'][0].get('institution_coordinates') if person['education'] else None

                                    if birth_coords and education_coords:
                                        distance_birth_to_education = calculate_distance(birth_coords, education_coords)
                                        if distance_birth_to_education is not None:
                                            total_distance_birth_to_education += distance_birth_to_education
                                            count_birth_to_education += 1

                                    if birth_coords and current_coords:
                                        distance_birth_to_current = calculate_distance(birth_coords, current_coords)
                                        if distance_birth_to_current is not None:
                                            total_distance_birth_to_current += distance_birth_to_current
                                            count_birth_to_current += 1

                                    if education_coords and current_coords:
                                        distance_education_to_current = calculate_distance(education_coords, current_coords)
                                        if distance_education_to_current is not None:
                                            total_distance_education_to_current += distance_education_to_current
                                            count_education_to_current += 1
                        except Exception as e:
                            print(f"Error processing file {file_path}: {e}")

# Calculate the average distances
average_distance_birth_to_education = total_distance_birth_to_education / count_birth_to_education if count_birth_to_education > 0 else None
average_distance_birth_to_current = total_distance_birth_to_current / count_birth_to_current if count_birth_to_current > 0 else None
average_distance_education_to_current = total_distance_education_to_current / count_education_to_current if count_education_to_current > 0 else None

print(f"Average distance from birthplace to education institution: {average_distance_birth_to_education} km")
print(f"Average distance from birthplace to current location: {average_distance_birth_to_current} km")
print(f"Average distance from education institution to current location: {average_distance_education_to_current} km")




# Plot histograms
plt.figure(figsize=(15, 5))

# Histogram for distances from birthplace to education institution
plt.subplot(1, 3, 1)
plt.hist(distances_birth_to_education, bins=20, color='blue', edgecolor='black')
plt.title('Birthplace to Education Institution')
plt.xlabel('Distance (km)')
plt.ylabel('Frequency')

# Histogram for distances from birthplace to current location
plt.subplot(1, 3, 2)
plt.hist(distances_birth_to_current, bins=20, color='green', edgecolor='black')
plt.title('Birthplace to Current Location')
plt.xlabel('Distance (km)')
plt.ylabel('Frequency')

# Histogram for distances from education institution to current location
plt.subplot(1, 3, 3)
plt.hist(distances_education_to_current, bins=20, color='red', edgecolor='black')
plt.title('Education Institution to Current Location')
plt.xlabel('Distance (km)')
plt.ylabel('Frequency')

# Display the histograms
plt.tight_layout()
plt.show()


def calculate_distances_for_occupation(occupation_hisco_code):
    # Define the base directory
    base_directory = "data/json_structured_geocoded_hisco"

    # Initialize variables to store total distances and counts
    total_distance_birth_to_education = 0
    total_distance_birth_to_current = 0
    total_distance_education_to_current = 0
    count_birth_to_education = 0
    count_birth_to_current = 0
    count_education_to_current = 0

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
                                    structured_data = bio_data['structured']

                                    for person_id, person in structured_data.items():
                                        occupation_code = person.get('occupation_hisco_code')
                                        if occupation_code == occupation_hisco_code:
                                            birth_coords = person['birth_details'].get('place_coordinates')
                                            current_coords = person.get('location_coordinates')
                                            education_coords = person['education'][0].get('institution_coordinates') if person['education'] else None

                                            if birth_coords and education_coords:
                                                distance_birth_to_education = calculate_distance(birth_coords, education_coords)
                                                if distance_birth_to_education is not None:
                                                    total_distance_birth_to_education += distance_birth_to_education
                                                    count_birth_to_education += 1

                                            if birth_coords and current_coords:
                                                distance_birth_to_current = calculate_distance(birth_coords, current_coords)
                                                if distance_birth_to_current is not None:
                                                    total_distance_birth_to_current += distance_birth_to_current
                                                    count_birth_to_current += 1

                                            if education_coords and current_coords:
                                                distance_education_to_current = calculate_distance(education_coords, current_coords)
                                                if distance_education_to_current is not None:
                                                    total_distance_education_to_current += distance_education_to_current
                                                    count_education_to_current += 1
                            except Exception as e:
                                print(f"Error processing file {file_path}: {e}")

    # Calculate the average distances
    average_distance_birth_to_education = total_distance_birth_to_education / count_birth_to_education if count_birth_to_education > 0 else None
    average_distance_birth_to_current = total_distance_birth_to_current / count_birth_to_current if count_birth_to_current > 0 else None
    average_distance_education_to_current = total_distance_education_to_current / count_education_to_current if count_education_to_current > 0 else None

    print(f"Average distance from birthplace to education institution: {average_distance_birth_to_education} km")
    print(f"Average distance from birthplace to current location: {average_distance_birth_to_current} km")
    print(f"Average distance from education institution to current location: {average_distance_education_to_current} km")


# Calculate distances for hisco code 34
calculate_distances_for_occupation(141)



# so we can say that on average, workers in hisco code 34 move further away from where they study to where they work - 400km on average.





def calculate_distances_for_occupation(occupation_hisco_code):
    # Define the base directory
    base_directory = "data/json_structured_geocoded_hisco"

    # Initialize lists to store distances
    distances_birth_to_education = []
    distances_birth_to_current = []
    distances_education_to_current = []

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
                                    structured_data = bio_data['structured']

                                    for person_id, person in structured_data.items():
                                        occupation_code = person.get('occupation_hisco_code')
                                        if occupation_code == occupation_hisco_code:
                                            birth_coords = person['birth_details'].get('place_coordinates')
                                            current_coords = person.get('location_coordinates')
                                            education_coords = person['education'][0].get('institution_coordinates') if person['education'] else None

                                            if birth_coords and education_coords:
                                                distance_birth_to_education = calculate_distance(birth_coords, education_coords)
                                                if distance_birth_to_education is not None:
                                                    distances_birth_to_education.append(distance_birth_to_education)

                                            if birth_coords and current_coords:
                                                distance_birth_to_current = calculate_distance(birth_coords, current_coords)
                                                if distance_birth_to_current is not None:
                                                    distances_birth_to_current.append(distance_birth_to_current)

                                            if education_coords and current_coords:
                                                distance_education_to_current = calculate_distance(education_coords, current_coords)
                                                if distance_education_to_current is not None:
                                                    distances_education_to_current.append(distance_education_to_current)
                            except Exception as e:
                                print(f"Error processing file {file_path}: {e}")

    # Create a DataFrame with the distances
    data = {
        'Birth to Education': distances_birth_to_education,
        'Birth to Current': distances_birth_to_current,
        'Education to Current': distances_education_to_current
    }
    distances_df = pd.DataFrame.from_dict(data, orient='index').transpose()

    return distances_df

# try it out with hisco code 211
distances_df = calculate_distances_for_occupation(34)




### Now add coords


def calculate_distances_for_occupation(occupation_hisco_code):
    # Define the base directory
    base_directory = "data/json_structured_geocoded_hisco"

    # Initialize lists to store distances and coordinates
    distances_birth_to_education = []
    distances_birth_to_current = []
    distances_education_to_current = []
    birth_coords_list = []
    current_coords_list = []
    education_coords_list = []

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
                                    structured_data = bio_data['structured']

                                    for person_id, person in structured_data.items():
                                        occupation_code = person.get('occupation_hisco_code')
                                        if occupation_code == occupation_hisco_code:
                                            birth_coords = person['birth_details'].get('place_coordinates')
                                            current_coords = person.get('location_coordinates')
                                            education_coords = person['education'][0].get('institution_coordinates') if person['education'] else None

                                            # Store coordinates
                                            birth_coords_list.append(birth_coords)
                                            current_coords_list.append(current_coords)
                                            education_coords_list.append(education_coords)

                                            if birth_coords and education_coords:
                                                distance_birth_to_education = calculate_distance(birth_coords, education_coords)
                                                if distance_birth_to_education is not None:
                                                    distances_birth_to_education.append(distance_birth_to_education)

                                            if birth_coords and current_coords:
                                                distance_birth_to_current = calculate_distance(birth_coords, current_coords)
                                                if distance_birth_to_current is not None:
                                                    distances_birth_to_current.append(distance_birth_to_current)

                                            if education_coords and current_coords:
                                                distance_education_to_current = calculate_distance(education_coords, current_coords)
                                                if distance_education_to_current is not None:
                                                    distances_education_to_current.append(distance_education_to_current)
                            except Exception as e:
                                print(f"Error processing file {file_path}: {e}")

    # Create a DataFrame with the distances and coordinates
    data = {
        'Birth to Education Distance': distances_birth_to_education,
        'Birth to Current Distance': distances_birth_to_current,
        'Education to Current Distance': distances_education_to_current,
        'Birth Coordinates': birth_coords_list,
        'Current Coordinates': current_coords_list,
        'Education Coordinates': education_coords_list
    }
    distances_df = pd.DataFrame(data)

    return distances_df

# try it out 
distances_df = calculate_distances_for_occupation(34)

distances_df

# Save distances_df with the hisco code as the filename
# create "data/distances" directory if it doesn't exist
Path("data/distances").mkdir(parents=True, exist_ok=True)
distances_df.to_json(f'data/distances/distances_34.json')

# export distances_df as an excel file, splitting the coordinates into their own columns first
distances_df[['Birth Latitude', 'Birth Longitude']] = pd.DataFrame(distances_df['Birth Coordinates'].tolist(), index=distances_df.index)
distances_df[['Current Latitude', 'Current Longitude']] = pd.DataFrame(distances_df['Current Coordinates'].tolist(), index=distances_df.index)
distances_df[['Education Latitude', 'Education Longitude']] = pd.DataFrame(distances_df['Education Coordinates'].tolist(), index=distances_df.index)


distances_df.to_excel(f'data/distances/distances_34.xlsx', index=False)

# loop through 12, 23, 34, 342, 841, 849, 851, 852, 853, 854, 855, 856, 857, 859, 961
# and save each distances_df to an excel file and make a function to do it
def save_distances_df(occupation_hisco_code):
    # create "data/distances" directory if it doesn't exist
    Path("data/distances").mkdir(parents=True, exist_ok=True)

    # calculate distances_df
    distances_df = calculate_distances_for_occupation(occupation_hisco_code)

    # save distances_df as a json file
    distances_df.to_json(f'data/distances/distances_{occupation_hisco_code}.json')

    # export distances_df as an excel file, splitting the coordinates into their own columns first
    distances_df[['Birth Latitude', 'Birth Longitude']] = pd.DataFrame(distances_df['Birth Coordinates'].tolist(), index=distances_df.index)
    distances_df[['Current Latitude', 'Current Longitude']] = pd.DataFrame(distances_df['Current Coordinates'].tolist(), index=distances_df.index)
    distances_df[['Education Latitude', 'Education Longitude']] = pd.DataFrame(distances_df['Education Coordinates'].tolist(), index=distances_df.index)
    distances_df.to_excel(f'data/distances/distances_{occupation_hisco_code}.xlsx', index=False)

# try 841
save_distances_df(851)

# loop through 12, 23, 34, 342, 841, 849, 851, 852, 853, 854, 855, 856, 857, 859, 961
# and save each distances_df to an excel file
for hisco_code in [12, 23, 34, 342, 841, 849, 851, 852, 853, 854, 855, 856, 857, 859, 961]:
    save_distances_df(hisco_code)

