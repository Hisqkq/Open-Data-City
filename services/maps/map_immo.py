import json
import dash_leaflet as dl

# Charger les données GeoJSON des quartiers
with open("services/data/processed/PlanningArea.geojson", "r") as f:
    areazone_data = json.load(f)


def create_map():
    return dl.Map(
                    center=[1.3521, 103.8198],
                    zoom=11,
                    children=[
                        dl.TileLayer(),
                        dl.GeoJSON(
                            data=areazone_data,
                            id="PlanningArea",
                            style={
                                "color": "blue",
                                "weight": 2,
                                "fillOpacity": 0.1,
                            },
                            hoverStyle={
                                "color": "red",
                                "weight": 3,
                            },
                        ),
                    ],
                    style={"height": "100%", "width": "100%"},
                )