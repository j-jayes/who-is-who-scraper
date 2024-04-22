# Step 1: Preparation
import pandas as pd
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
import json
import os
from pathlib import Path
from collections import Counter

# read in hisco from data/occupations/3-digit-hisco.xlsx
hisco = pd.read_excel('data/occupations/3-digit-hisco.xlsx')

hisco.columns

# make a dataframe that we can get the embeddings for 
occupations = hisco['name'].to_list()

# select first 5 occupations
# occupations = occupations[:10]

# Step 2: Embedding


# set up model
model = SentenceTransformer('KBLab/sentence-bert-swedish-cased')

model_name = 'KBLab_sentence-bert-swedish-cased'

# Check if embeddings already exist in the cache file
cache_file_path = f'data/clustering/embeddings_{model_name}.json'

if os.path.exists(cache_file_path):
    # Read embeddings from the cache file
    with open(cache_file_path, 'r', encoding='utf-8') as file:
        embeddings = json.load(file)
else:
    # Generate embeddings for the concatenated texts
    embeddings = model.encode(occupations, convert_to_tensor=True)
    # Save embeddings to the cache file
    os.makedirs('data/clustering', exist_ok=True)
    with open(cache_file_path, 'w', encoding='utf-8') as file:
        json.dump(embeddings.tolist(), file, ensure_ascii=False, indent=4)

# join embeddings back to hisco name, if the embeddings are already a list we don't need to convert them
if isinstance(embeddings, list):
    hisco_embeddings = pd.DataFrame({'name': occupations, 'embeddings': embeddings})
else:
    hisco_embeddings = pd.DataFrame({'name': occupations, 'embeddings': embeddings.tolist()})

# save to data/occupations/hisco_embeddings.json
hisco_embeddings.to_json('data/occupations/hisco_embeddings.json')





# Now we want to get the titles from the biographies and save them as a dataframe
# We can do this by looping through the json files and extracting the titles

# Define the base directory
base_directory = "data/json_structured_geocoded"

def extract_occupations(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

    occupations = []
    for key, person_data in data.get('structured', {}).items():
        if isinstance(person_data, dict):
            # Extract current occupation
            current_occupation= person_data.get('occupation', '')
            if current_occupation and isinstance(current_occupation, str):
                occupations.append(current_occupation)

    return occupations



def create_occupations_cache(base_dir, cache_file):
    occupations_counter = Counter()

    for book_name in os.listdir(base_dir):
        book_path = os.path.join(base_dir, book_name)
        if os.path.isdir(book_path):
            for letter in os.listdir(book_path):
                letter_path = os.path.join(book_path, letter)
                if os.path.isdir(letter_path):
                    for filename in os.listdir(letter_path):
                        if filename.endswith(".json"):
                            file_path = os.path.join(letter_path, filename)
                            locations = extract_occupations(file_path)
                            for location in locations:
                                occupations_counter.update([location])  # Update with individual location

    # Save locations and counts to cache file
    Path(os.path.dirname(cache_file)).mkdir(parents=True, exist_ok=True)
    with open(cache_file, "w") as outfile:
        json.dump(dict(occupations_counter), outfile, indent=4, ensure_ascii=False)


# Define the base directory and cache file path
base_directory = "data/json_structured_geocoded"
cache_file_path = "data/occupations/extracted_occupations_cache.json"

# ensure cache directory exists
Path(os.path.dirname(cache_file_path)).mkdir(parents=True, exist_ok=True)

# Create the locations cache
create_occupations_cache(base_directory, cache_file_path)


# now we want to get the embeddings for the occupations in the occupations cache
# first we read in the occupations cache
with open(cache_file_path, 'r', encoding='utf-8') as file:
    occupations = json.load(file)

# next we create a function to get the embeddings for each occupation
def generate_occupation_embedding(occ_string):
    # Generate embeddings for the concatenated texts
    embedding = model.encode(occ_string, convert_to_tensor=True)
    return embedding

# now we want to loop through the occupations and get the embeddings
# we can do this by looping through the occupations dictionary
# and then using the generate_occupation_embedding function
# we then want to save the embeddings to a dataframe
# and then save the dataframe to a json file

# create empty list to store embeddings
occupation_embeddings = []

# loop through occupations
for occ in occupations:
    # get the embedding for the occupation
    embedding = generate_occupation_embedding(occ)
    # print the occupation and first few characters of the embedding
    print(occ, embedding[:5])
    # append the occupation and embedding to the list
    occupation_embeddings.append({'occupation': occ, 'embedding': embedding.tolist()})

# save the list to a dataframe
occupation_embeddings_df = pd.DataFrame(occupation_embeddings)

# save the dataframe to a json file while setting ensure_ascii to False
with open('data/occupations/occupation_embeddings.json', 'w', encoding='utf-8') as f:
    json.dump(occupation_embeddings_df.to_dict(), f, ensure_ascii=False, indent=4)


# Now we want to find the closest occupation for each occupation in the hisco dataset
# We can do this by looping through the hisco dataset and calculating the cosine distance
# between the hisco occupation and the occupations in the occupation embeddings dataset
# We then want to save the closest occupation to the hisco dataset for each occupation in the occupation embeddings dataset

# read in the hisco embeddings
hisco_embeddings = pd.read_json('data/occupations/hisco_embeddings.json')

# read in the occupation embeddings
occupation_embeddings = pd.read_json('data/occupations/occupation_embeddings.json')

# save a sample of the occupation embeddings which is 5 rows
occupation_embeddings_sample = occupation_embeddings.sample(5)

# save the dataframe to a json file while setting ensure_ascii to False
with open('data/occupations/occupation_embeddings_sample.json', 'w', encoding='utf-8') as f:
    json.dump(occupation_embeddings_sample.to_dict(), f, ensure_ascii=False, indent=4)
