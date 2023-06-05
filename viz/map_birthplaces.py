import os
import json
import folium
import branca
from collections import Counter

input_directory = "data/biographies_augmented"

# Read the biography files and create a list of dictionaries with the required data
biographies = []
for file_name in os.listdir(input_directory):
    file_path = os.path.join(input_directory, file_name)
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    structured_data = data["structured"]
    if "name" in structured_data and "birthPlace" in structured_data and "latitude" in structured_data["birthPlace"]:
        education_info = structured_data.get("education", [])
        education_names = [edu["name"] for edu in education_info if isinstance(edu, dict) and "name" in edu]

        biographies.append({
            "name": structured_data["name"],
            "birthPlace": structured_data["birthPlace"],
            "jobTitle": structured_data.get("jobTitle", "Unknown"),
            "education": education_names
        })


# Count the job titles
job_titles = [bio["jobTitle"] if not isinstance(bio["jobTitle"], list) else "Unknown" for bio in biographies]
job_title_counts = Counter(job_titles)

# Get the top 6 most common job titles
top_job_titles = [title for title, _ in job_title_counts.most_common(6)]

# Assign the category "other" to job titles not in the top 6
for bio in biographies:
    if bio["jobTitle"] not in top_job_titles:
        bio["jobTitle"] = "other"

# Create a folium Map object centered around Sweden
map_sweden = folium.Map(location=[62.198337, 17.551337], zoom_start=5)

# Create a FeatureGroup for each job title
feature_groups = {}
for job_title in set(top_job_titles + ["other"]):
    feature_group = folium.FeatureGroup(name=job_title)
    feature_groups[job_title] = feature_group

# Add markers to the map for each person's birthplace
for bio in biographies:
    birthplace = bio["birthPlace"]
    popup_text = f"<strong>Name:</strong> {bio['name']}<br><strong>Job Title:</strong> {bio['jobTitle']}<br><strong>Education:</strong> {', '.join(bio['education'])}"
    marker = folium.Marker(
        location=[birthplace["latitude"], birthplace["longitude"]],
        popup=folium.Popup(popup_text, max_width=250)
    )
    feature_groups[bio["jobTitle"]].add_child(marker)


# Add the feature groups to the map
for feature_group in feature_groups.values():
    feature_group.add_to(map_sweden)

# Create a LayerControl to select/deselect job titles
folium.LayerControl(collapsed=False).add_to(map_sweden)

# Save the map as an HTML file
map_sweden.save("sweden_map_checkboxes.html")
