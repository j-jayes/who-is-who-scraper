import pandas as pd
from math import radians, cos, sin, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance between two points on the Earth."""
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    r = 6371  # Radius of Earth in kilometers
    return c * r

def skip_haversine(lat1, lon1, lat2, lon2):
    """Skip calculations for specific coordinate values."""
    skip_lat = 59.32932
    skip_lon = 18.06858
    if any(v == skip_lat for v in [lat1, lat2]) or any(v == skip_lon for v in [lon1, lon2]):
        return None
    else:
        return haversine(lat1, lon1, lat2, lon2)

def calculate_distances(data):
    """Calculate distances between locations, handling missing and specific coordinate values."""
    data['distance_current_to_institution'] = data.apply(
        lambda row: skip_haversine(row['current_lat'], row['current_lon'], row['institution_lat'], row['institution_lon']), axis=1
    )
    data['distance_birth_to_institution'] = data.apply(
        lambda row: skip_haversine(row['birth_lat'], row['birth_lon'], row['institution_lat'], row['institution_lon']), axis=1
    )
    data['distance_birth_to_current'] = data.apply(
        lambda row: skip_haversine(row['birth_lat'], row['birth_lon'], row['current_lat'], row['current_lon']), axis=1
    )
    return data

def main():
    file_path = 'data/occupations/individual_occupations_institution_geocoded.csv'
    file_path_out = 'data/occupations/individual_occupations_institution_geocoded_distances.csv'
    data = pd.read_csv(file_path)
    result = calculate_distances(data)
    result.to_csv(file_path_out, index=False)
    

if __name__ == "__main__":
    main()
