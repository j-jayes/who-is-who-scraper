
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Function to load JSON file
def load_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to calculate cosine similarity
def calculate_cosine_similarity(vec1, vec2):
    return cosine_similarity(vec1.reshape(1, -1), vec2.reshape(1, -1))[0][0]

# Function to find the closest Hisco code for each occupation
def find_closest_hisco(occupation_embeddings, hisco_embeddings, hisco_names):
    closest_matches = {}
    for occ_id, occ_embed in occupation_embeddings.items():
        highest_similarity = -1
        closest_hisco = None
        for hisco_id, hisco_embed in hisco_embeddings.items():
            similarity = calculate_cosine_similarity(occ_embed, hisco_embed)
            if similarity > highest_similarity:
                highest_similarity = similarity
                closest_hisco = hisco_id
                # print closest match
                print(f"Closest match for {occ_id} is {hisco_id} with similarity {highest_similarity}")
        closest_matches[occ_id] = {
            'closest_hisco': closest_hisco, 
            'cosine_similarity': highest_similarity,
            'hisco_occupation': hisco_names[closest_hisco]
        }
    return closest_matches


occupation_embeddings = load_json_file('data/occupations/occupation_embeddings.json')
hisco_embeddings = load_json_file('data/occupations/hisco_embeddings.json')

# Extracting embeddings and names
occupation_names = occupation_embeddings['occupation']
occupation_embeds = occupation_embeddings['embedding']
occupation_embeddings_dict = {k: np.array(occupation_embeds[k]) for k in occupation_names}

hisco_names = hisco_embeddings['name']
hisco_embeds = hisco_embeddings['embeddings']
hisco_embeddings_dict = {k: np.array(hisco_embeds[k]) for k in hisco_names}

# Finding the closest Hisco code for each occupation
closest_hisco_matches = find_closest_hisco(occupation_embeddings_dict, hisco_embeddings_dict, hisco_names)

# join the occupation names to the closest matches
closest_hisco_matches = {occupation_names[k]: v for k, v in closest_hisco_matches.items()}



# There needs to be a lookup table here to replace the closest_hisco number from an index to the hisco code from the file
# read in the hisco codes
hisco_codes = pd.read_excel("data/occupations/3-digit-hisco.xlsx")

# select the column we want, number
hisco_codes = hisco_codes[['number']]
# rename it to hisco_code 
hisco_codes.columns = ['hisco_code']

# Make a column called "closest_hisco" from the index in hisco_codes
hisco_codes['closest_hisco'] = hisco_codes.index
# make closest_hisco an integer
hisco_codes['closest_hisco'] = hisco_codes['closest_hisco'].astype(int)

# create closest_hisco_matches_df from closest_hisco_matches
closest_hisco_matches_df = pd.DataFrame(closest_hisco_matches).transpose()

# make the index a column and call it "occupation"
closest_hisco_matches_df = closest_hisco_matches_df.reset_index().rename(columns={'index': 'occupation'})
# make closest_hisco an integer
closest_hisco_matches_df['closest_hisco'] = closest_hisco_matches_df['closest_hisco'].astype(int)

# join the closest_hisco_matches_df to hisco_codes on "closest_hisco" with
closest_hisco_matches_df = closest_hisco_matches_df.merge(hisco_codes, on='closest_hisco', how='left')

# drop the "closest_hisco" column
closest_hisco_matches_df = closest_hisco_matches_df.drop(columns=['closest_hisco'])

closest_hisco_matches_df.columns


# save the closest_hisco_matches_df to a json file with ensure_ascii=False
with open('data/occupations/closest_hisco_matches.json', 'w', encoding='utf-8') as f:
    json.dump(closest_hisco_matches_df.to_dict(), f, ensure_ascii=False, indent=4)

