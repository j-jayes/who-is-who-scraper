
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

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

# save the closest matches to a json file
with open('data/occupations/closest_hisco_matches.json', 'w', encoding='utf-8') as f:
    json.dump(closest_hisco_matches, f, ensure_ascii=False, indent=4)

