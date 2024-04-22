# Geocode institutions
import json
import os
from collections import Counter
from pathlib import Path
import requests
from dotenv import load_dotenv
import pandas as pd
import requests

load_dotenv()

df = pd.read_csv('data/occupations/individual_occupations.xlsx')

# count institutions
institutions = df['institution'].value_counts().reset_index()

# take the first 300 institutions
institutions = institutions.head(300)

# write to excel
institutions.to_excel('data/degrees/institutions_top_300_to_geocode.xlsx', index=False)

institutions_to_geocode = pd.read_excel('data/degrees/institutions_top_300_to_geocode_corrected.xlsx')

# Google Maps Geocoding API key from .env
api_key = os.getenv('GOOGLE_MAPS_API_KEY')

# Define the geocoding function
def geocode(address, api_key):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'address': address, 'key': api_key}
    response = requests.get(url, params=params)
    data = response.json()
    if data['status'] == 'OK':
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        print(f"Geocoded {address} as {lat}, {lng}")
        return lat, lng
    else:
        return None, None


# Apply the geocode function to the 'institution_to_geocode' column
institutions_to_geocode['coordinates'] = institutions_to_geocode['institution_to_geocode'].apply(geocode, api_key=api_key)

# Split the coordinates into two columns
institutions_to_geocode[['institution_lat', 'institution_lon']] = pd.DataFrame(institutions_to_geocode['coordinates'].tolist(), index=institutions_to_geocode.index)

# Drop the 'coordinates' column as it's no longer needed
institutions_to_geocode.drop('coordinates', axis=1, inplace=True)

# Save the DataFrame to an Excel file
institutions_to_geocode.to_excel('data/degrees/geocoded_institutions_top.xlsx', index=False)