import dash
import dash_mantine_components as dmc
from dash import dcc, callback, Output, Input
import plotly.express as px

dash.register_page(__name__, path="/visualisation")

df = px.data.gapminder()
dff = df[df.year == 2007]

dmc.add_figure_templates()

# Exemple de données
data = [
    {"month": "January", "Smartphones": 1200, "Laptops": 900, "Tablets": 200},
    {"month": "February", "Smartphones": 1900, "Laptops": 1200, "Tablets": 400},
    {"month": "March", "Smartphones": 400, "Laptops": 1000, "Tablets": 200},
    {"month": "April", "Smartphones": 1000, "Laptops": 200, "Tablets": 800},
    {"month": "May", "Smartphones": 800, "Laptops": 1400, "Tablets": 1200},
    {"month": "June", "Smartphones": 750, "Laptops": 600, "Tablets": 1000}
]

# 📌 Layout avec les graphiques
layout = dmc.Container(
    dmc.SimpleGrid(
        [
            # 🔵 Graphique Plotly avec changement de thème
            dmc.Stack(
                [
                    dmc.Text("Plotly Express Bar Chart", size="xl", style={"align" : "center"}),  # 🔥 Ajout du titre
                    dcc.Graph(id="bar-chart"), 
                ],
            ),

            # 🟣 Graphique Mantine
            dmc.Stack(
                [
                    dmc.Text("Mantine Bar Chart", size="xl", style={"align" : "center"}),  # 🔥 Ajout du titre
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
        cols=2
    ),
    style={"padding": "1rem"},
)

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
