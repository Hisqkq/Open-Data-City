import dash
import dash_mantine_components as dmc
from dash import dcc, html, callback, Output, Input
import copy
import plotly.express as px
from services.maps.planning_area import generate_singapore_map, load_and_process_geojson, update_map_background

# 📌 Permet d'ignorer les erreurs de composants dynamiques
dash.register_page(__name__, path="/visualisation", suppress_callback_exceptions=True)

df = px.data.gapminder()
dff = df[df.year == 2007]

dmc.add_figure_templates()

# 📌 Charger les données GeoJSON et DataFrame une seule fois
geojson_path = "services/data/processed/PlanningArea.geojson"
planning_df, geojson_data = load_and_process_geojson(geojson_path)

# ✅ On génère la carte une seule fois (sans callback)
base_fig = generate_singapore_map(planning_df, geojson_data)

# Exemple de données
data = [
    {"month": "January", "Smartphones": 1200, "Laptops": 900, "Tablets": 200},
    {"month": "February", "Smartphones": 1900, "Laptops": 1200, "Tablets": 400},
    {"month": "March", "Smartphones": 400, "Laptops": 1000, "Tablets": 200},
    {"month": "April", "Smartphones": 1000, "Laptops": 200, "Tablets": 800},
    {"month": "May", "Smartphones": 800, "Laptops": 1400, "Tablets": 1200},
    {"month": "June", "Smartphones": 750, "Laptops": 600, "Tablets": 1000}
]

# 📌 Layout optimisé avec chargement asynchrone
layout = dmc.Container(
    [
        dmc.SimpleGrid(
            [
                # 🔵 Graphique Plotly Express
                dmc.Stack(
                    [
                        dmc.Text("Plotly Express Bar Chart", size="xl"),
                        dcc.Graph(id="bar-chart"),
                    ],
                ),

                # 🟣 Graphique Mantine
                dmc.Stack(
                    [
                        dmc.Text("Mantine Bar Chart", size="xl"),
                        dmc.BarChart(
                            h=500,
                            dataKey="month",
                            data=data,
                            series=[
                                {"name": "Smartphones", "color": "violet.6"},
                                {"name": "Laptops", "color": "blue.6"},
                                {"name": "Tablets", "color": "teal.6"}
                            ],
                            tickLine="y",
                            gridAxis="y",
                            withXAxis=True,
                            withYAxis=True,
                        ),
                    ],
                ),
            ],
            cols=2,
        ),
        # 📌 Loader pour la carte Mapbox (évite un ralentissement au démarrage)
        dcc.Loading(
            id="loading-map",
            type="circle",
            children=[
                dcc.Graph(id="map-plotly", figure=base_fig, config={"scrollZoom": True}),  
            ],
        ),
    ],
    style={"padding": "1rem"},
)

@callback(
    Output("map-plotly", "figure"),
    Input("theme-store", "data")
)
def update_map_style(theme):
    # Créer une copie de la figure de base pour éviter de modifier l'objet global
    fig = base_fig
    return update_map_background(fig, theme)


# 🔄 Callback pour changer le thème du graphique en fonction du mode sombre/claire
@callback(
    Output("bar-chart", "figure"),
    Input("theme-store", "data"),  
)
def update_graph(theme):
    template = "mantine_dark" if theme == "dark" else "mantine_light"

    fig = px.bar(
        dff,
        x="continent",
        y="pop",
        template=template,  # 🔥 Mise à jour dynamique du template
    )

    return fig
