import json

# Charger les données GeoJSON

def load_geojson():
    with open("services/data/raw/communes.geojson", "r") as f:
        communes_data = json.load(f)
    return communes_data

