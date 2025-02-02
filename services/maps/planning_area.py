import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 📌 Charger et traiter les données GeoJSON
def load_and_process_geojson(geojson_path="services/data/processed/PlanningArea.geojson"):
    with open(geojson_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 📌 Extraire les noms des Planning Areas
    planning_areas = []
    for feature in data["features"]:
        name = feature["properties"].get("PLN_AREA_N", "Unknown")
        planning_areas.append({"PLN_AREA_N": name})

    return pd.DataFrame(planning_areas), data

def generate_singapore_map(df, geojson_data):
    """
    Génère la carte interactive avec contours visibles et surbrillance dynamique (non implémentée en hover).
    
    Args:
        df (pd.DataFrame): DataFrame contenant les noms des zones.
        geojson_data (dict): Données GeoJSON pour l'affichage.
    
    Returns:
        go.Figure: Figure Plotly interactive.
    """
    fig = px.choropleth_mapbox(
        df,
        geojson=geojson_data,
        locations="PLN_AREA_N",
        featureidkey="properties.PLN_AREA_N",
        hover_name="PLN_AREA_N",
        center={"lat": 1.3521, "lon": 103.8198},
        zoom=10,
        opacity=0.6,
    )

    # Appliquer un contour noir par défaut et personnaliser le hover
    fig.update_traces(
        marker_line_width=1.5,
        marker_line_color="black",  # Bordure noire par défaut
        hovertemplate="<b>%{location}</b>",
        hoverlabel=dict(bgcolor="white", font_size=14, font_family="Arial"),
        hoverinfo="location+text",
    )

    # Supprimer la légende et ajuster les marges
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
    )

    return fig


# 📌 Met à jour uniquement le **fond** sans redessiner les polygones
def update_map_background(fig, theme):
    """
    Modifie uniquement le fond de la carte sans redessiner les données.

    Args:
        fig (go.Figure): Figure Plotly existante.
        theme (str): "light" ou "dark" pour changer le style Mapbox.

    Returns:
        go.Figure: Figure mise à jour.
    """
    mapbox_style = "carto-positron" if theme == "light" else "carto-darkmatter"

    fig.update_layout(mapbox_style=mapbox_style)  # ✅ Change juste le fond

    return fig
