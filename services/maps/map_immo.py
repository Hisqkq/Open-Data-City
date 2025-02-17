import json
import dash_leaflet as dl

from utils.config import TOWNS

with open("services/data/processed/PriceWithHistory.geojson", "r") as f:
    areazone_data = json.load(f)


def filter_geojson_by_towns(geojson, towns):
    allowed = {town["value"].strip() for town in towns}
    filtered_features = [
        feature for feature in geojson["features"]
        if feature["properties"].get("PLN_AREA_N", "").strip() in allowed
    ]
    geojson["features"] = filtered_features
    return geojson

def create_map():
    with open("services/data/processed/PriceWithHistory.geojson", "r", encoding="utf-8") as f:
        geojson = json.load(f)
    
    geojson_filtered = filter_geojson_by_towns(geojson, TOWNS)
    
    return dl.Map(
        center=[1.3521, 103.8198],
        zoom=11,
        children=[
            dl.TileLayer(),
            dl.GeoJSON(
                data=geojson_filtered,
                id="geojson-layer",
                style={"color": "blue", "weight": 2, "fillOpacity": 0.1},
                hoverStyle={"color": "red", "weight": 3},
                interactive=True,
            ),
        ],
        style={"height": "100%", "width": "100%"},
    )
