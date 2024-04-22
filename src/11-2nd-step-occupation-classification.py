# Step 1: Preparation
import pandas as pd
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
import json
import os
from pathlib import Path
from collections import Counter

# read in hisco from data/occupations/3-digit-hisco.xlsx
hisco = pd.read_excel('data/careers/industrial_groupings.xlsx')

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
cache_file_path = f'data/clustering/embeddings_{model_name}_sectors.json'

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
hisco_embeddings.to_json('data/careers/sector_embeddings.json')







import json
import os
from pathlib import Path

def format_career_info(position, organization):
    """
    Concatenates position and organization, replacing 'Unknown', 'NULL', or 'None' with an empty string.
    """
    if position in ["Unknown", "NULL", "None"]:
        position = ""
    if organization in ["Unknown", "NULL", "None"]:
        organization = ""
    
    career_info = f"{position} {organization}".strip()
    return career_info

def extract_career_trajectories(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

    last_careers = []
    for key, person_data in data.get('structured', {}).items():
        if isinstance(person_data, dict):
            career_data = person_data.get('career', [])
            if isinstance(career_data, list) and career_data:
                last_career = career_data[-1]
                if isinstance(last_career, dict):
                    last_position = last_career.get('position', 'Unknown')
                    last_organization = last_career.get('organization', 'Unknown')
                    career_info = format_career_info(last_position, last_organization)
                    last_careers.append({'id': key, 'position': last_position, 'organization': last_organization, 'career_info': career_info})
            elif isinstance(career_data, str):
                career_info = format_career_info(career_data, 'Unknown')
                last_careers.append({'id': key, 'position': career_data, 'organization': 'Unknown', 'career_info': career_info})

    return last_careers

def create_career_cache(base_dir, cache_file):
    career_cache = []

    for book_name in os.listdir(base_dir):
        book_path = os.path.join(base_dir, book_name)
        if os.path.isdir(book_path):
            for letter in os.listdir(book_path):
                letter_path = os.path.join(book_path, letter)
                if os.path.isdir(letter_path):
                    for filename in os.listdir(letter_path):
                        if filename.endswith(".json"):
                            file_path = os.path.join(letter_path, filename)
                            last_careers = extract_career_trajectories(file_path)
                            career_cache.extend(last_careers)

    # Save the last careers to cache file
    Path(os.path.dirname(cache_file)).mkdir(parents=True, exist_ok=True)
    with open(cache_file, "w") as outfile:
        json.dump(career_cache, outfile, indent=4, ensure_ascii=False)

# Define the base directory and cache file path
base_directory = "data/json_structured_geocoded"
cache_file_path = "data/careers/last_careers_cache.json"

# Create the career cache
create_career_cache(base_directory, cache_file_path)






# now we want to get the embeddings for the occupations in the occupations cache
# first we read in the occupations cache
with open(cache_file_path, 'r', encoding='utf-8') as file:
    careers = json.load(file)

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

# Create an empty list to store embeddings
career_embeddings = []

# Loop through the careers
for career in careers:
    # Get the career_info
    occ = career['career_info']
    # Generate the embedding for the occupation
    embedding = generate_occupation_embedding(occ)
    # Print the occupation and first few characters of the embedding
    print(occ, embedding[:5])
    # Append the occupation and embedding to the list
    career_embeddings.append({'occupation': occ, 'embedding': embedding.tolist()})
# save the list to a dataframe
career_embeddings_df = pd.DataFrame(career_embeddings)

# save the dataframe to a json file while setting ensure_ascii to False
with open('data/careers/career_embeddings.json', 'w', encoding='utf-8') as f:
    json.dump(career_embeddings_df.to_dict(), f, ensure_ascii=False, indent=4)



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
