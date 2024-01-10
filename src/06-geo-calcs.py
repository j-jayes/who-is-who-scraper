import os
import json
from geopy.distance import geodesic
import statistics
import matplotlib.pyplot as plt

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

