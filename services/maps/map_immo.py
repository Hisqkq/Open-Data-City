import json
import dash_leaflet as dl
import re
import os
from services.data.process_data_immo import get_income_mapping, get_color_scale

# Charger les données GeoJSON des quartiers
with open("services/data/processed/areazone.geojson", "r") as f:
    areazone_data = json.load(f)

def get_color(area_name, income_mapping, color_scale):
    income = income_mapping.get(area_name, 500)  # Si inconnu, valeur basse par défaut
    return color_scale(income)  # Convertit le revenu en couleur

def create_map():
    income_mapping = get_income_mapping()
    color_scale = get_color_scale()

    return dl.Map(
        center=[1.3521, 103.8198],  # Singapour
        zoom=11,
        children=[
            dl.TileLayer(),
            dl.GeoJSON(
                data=areazone_data,
                id="areazone-geojson",
                style=lambda feature: {
                    "color": "black",
                    "weight": 1,
                    "fillColor": get_color(feature["properties"]["PLN_AREA_N"], income_mapping, color_scale),
                    "fillOpacity": 0.7,
                },
                hoverStyle={"color": "yellow", "weight": 3},
            ),
            # Ajouter la légende des couleurs
            color_scale,
        ],
        style={"height": "100%", "width": "100%"},
    )