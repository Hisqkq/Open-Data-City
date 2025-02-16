import dash
import dash_mantine_components as dmc
from dash import dcc, html
from dash_extensions import Lottie
import plotly.express as px
import dash_leaflet as dl
from dash import Output, Input, dcc, State
import pandas as pd
from figures.immobilier_fig import create_line_chart_figure_introduction, create_table_figure_introduction, create_line_chart_figure_history_price, create_bar_chart_figure
from services.maps.map_immo import create_map

dash.register_page(__name__, path="/immobilier")

layout = dmc.Container(
    fluid=True,
    p="xl",
    children=[

        html.Div(
            dmc.Title("Real estate indicators", order=1, style={"marginBottom": "1rem", "textAlign": "center"}),
            style={"width": "100%"},
            className="scroll-section",
        ),
        
        # ----------------------
        # En-tête avec titre et animation Lottie
        # ----------------------
        dmc.Paper(
            style={
                "display": "flex",
                "gap": "1rem",
                "alignItems": "top",
                "marginBottom": "1rem"
            },
            className="scroll-section",
            children=[
                dmc.Paper(
                    style={"width": "75%"},
                    children=[
                        dmc.Title("Singapore and the Soaring Real Estate Market!", order=1, style={"color": "#f6efed"}),
                        dmc.Text(
                            "Since 2017, Singapore’s property prices have seen a significant increase, reflecting the complex dynamics of the real estate market in one of the world’s most densely populated cities.",
                            size="lg",
                            style={"color": "#f6efed"}
                        ),
                        dmc.Text(
                            "As the price per square meter continues to rise, the question arises: how does this trend impact housing affordability for residents?",
                            size="lg",
                            style={"color": "#f6efed"}
                        ),
                        dmc.Text(
                            "Through this analysis, we will explore key figures, regional disparities, and future predictions to better understand the real estate challenges in Singapore.",
                            size="lg",
                            style={"color": "#f6efed"}
                        ),
                    ]
                ),

                dmc.Paper(
                    style={"width": "25%"},
                    children=[
                        Lottie(
                            options=dict(
                                loop=True,
                                autoplay=True,
                                rendererSettings=dict(preserveAspectRatio="xMidYMid slice")
                            ),
                            width="100%",
                            url="assets/img/Animation - 1738836928686.json"
                        )
                    ]
                ),
            ]
        ),
        dmc.Space(h="xl"),
        
        # ---------- Section 1 :  ----------
        dmc.Card(
            shadow="sm",
            withBorder=True,
            padding="lg",
            className="scroll-section",
            children=[
                dmc.Title("Price per Square Metre Over the Last 8 Years", order=2),
                dmc.Space(h="md"),
                dmc.Text(
                    "A spectacular surge in property prices! Since mid-2020, prices per square meter have experienced a meteoric rise, accelerating at an unprecedented pace. While they seemed relatively stable before this period, the trend reversed, leading to an almost continuous increase. How far will this price hike go? Will we see a slowdown or correction in the years to come?",
                    size="md",
                    style={
                        "lineHeight": "1.6",
                        "textAlign": "justify"
                    }
                ),
                dmc.Space(h="md"),
                dmc.Paper(
                    children=[
                            create_line_chart_figure_introduction()
                            ],
                          ),
                dmc.Space(h="md"),
                dmc.Paper(
                    style={
                        "width": "75%",
                        "margin": "left",
                        "display": "block",  # Assure que le groupe est un bloc pour centrer correctement
                        "marginLeft": "5px",  # Marge à gauche
                        "marginRight": "10px",  # Marge à droite
                        },
                    children=[
                        dmc.Text(
                            """
                            The graph illustrates the evolution of the price per square meter over the last eight years. Three distinct phases can be observed.
                            """,
                            style={"marginBottom": "10px"}
                        ),
                        dmc.Text(
                            """
                            Between 2017 and mid-2020, prices remained relatively stable, fluctuating between €4,500 and €4,700/m², without significant variation.
                            This period of stagnation seems to mark a balance between supply and demand.
                            """,
                            style={"marginBottom": "10px"}
                        ),
                        dmc.Text(
                            """
                            From mid-2020 to 2021, a major turning point occurred. Prices began to rise dramatically, quickly exceeding €5,000/m²
                            in just a few months. This sudden increase coincided with the end of the health crisis, marking a new dynamic in the real estate market.
                            """,
                            style={"marginBottom": "10px"}
                        ),
                        dmc.Text(
                            """
                            From 2022 to today, the upward trend has not slowed down. On the contrary, prices continue to accelerate, reaching more than €7,000/m² in 2025,
                            a historic record that reflects strong pressure on the market.
                            """,
                            style={"marginBottom": "10px"}
                        ),
                        dmc.Text(
                            """
                            Several factors can explain this surge in prices. First, the post-COVID period has led to an economic recovery and changes in
                            purchasing habits, with increased demand for certain types of properties. Then, inflation and rising construction costs have
                            had a strong impact on the price of new projects, limiting supply and fueling price increases. Finally, the growing attractiveness of certain areas
                            has led to an influx of buyers, further increasing pressure on the market.
                            """,
                            style={"marginBottom": "10px"}
                        ),
                        dmc.Text(
                            "Will this trend continue, or are we on the verge of a market turnaround?",
                            style={"fontWeight": "bold"}
                        ),
                    ],
                    className="scroll-section",
                ),
                # dmc.Image(
                #     src="assets/img/dollar-de-singapour.png",  # Remplacez par le chemin de votre image
                #     radius="md",
                # ),
            ]
        ),
        dmc.Space(h="xl"),


        # ---------- Section 1 :  ----------
        dmc.Card(
            shadow="sm",
            withBorder=True,
            padding="lg",
            className="scroll-section",
            children=[
                dmc.Title("Number of homes costing more than a million dollars at resale", order=2),
                dmc.Space(h="md"),
                dmc.Text(
                    """
                    The high-end real estate market in Singapore is experiencing a meteoric rise. The number of homes resold for more than S$1 million has literally exploded in recent years. Until 2019, these transactions remained relatively rare, with less than 100 sales per year. But from 2021, the market is taking off, exceeding 200 and then 400 sales per year.
                    """,
                    size="md",
                    style={
                        "lineHeight": "1.6",
                        "textAlign": "justify"
                    }
                ),
                dmc.Space(h="md"),
                dmc.Paper(create_table_figure_introduction(), id="immo1-table-container"),
                dmc.Space(h="md"),
                dmc.Text(
                    """
                    The evolution of the figures is striking. In 2020, only 77 properties exceeded this symbolic bar, but by 2021, this number tripled to reach 233. The trend is only increasing with 426 sales in 2023, and an impressive record of 940 in 2024!

                    And what about 2025? With data only for January and February, there have already been 120 sales. That's almost twice as many as the whole of 2020! If this momentum continues, 2025 could well set a new record.

                    🔎 What are the reasons for this surge?
                    Several factors explain this rise in power. The growing appeal of Singapore as an economic hub, the increase in real estate prices, demand from foreign investors and a limited supply of exceptional properties are fueling this frenzy. The question now is: how far will it go?
                    """,
                    size="md",
                    style={
                        "lineHeight": "1.6",
                        "textAlign": "justify",
                        "marginBottom": "1rem"
                    }
                ),
            ]
        ),
        dmc.Space(h="xl"),

        # ----------------------
        # Section : Carte avec le switch
        # ----------------------

        dmc.Card(
            shadow="sm",
            withBorder=True,
            padding="lg",
            className="scroll-section",
            children=[
                dmc.Title("Working Residents by Salary and Price per square meter", order=2),
                dmc.Space(h="md"),
                dmc.Text(
                    "This map shows the distribution of salaries with either the resale price or the price per square meter",
                    size="md",
                    style={
                        "lineHeight": "1.6",
                        "textAlign": "justify"
                    }
                ),
                dmc.Space(h="md"),
                dmc.SegmentedControl(
                            id="resale_or_pricem2",
                            value="ng",
                            data=[
                                {"value": "Resale", "label": "Resale"},
                                {"value": "Price", "label": "Price per m²"},
                            ],
                            mb=10,
                        ),
                dmc.Space(h="md"),
                dcc.Store(id="selected_map", data="services/maps/folium_map_resale.html"),  # Stocke l'URL du fichier
                dcc.Loading(  # Effet de chargement pendant le changement de carte
                    type="circle",
                    children=html.Iframe(
                        id="map_iframe",
                        srcDoc=open("services/maps/folium_map_resale.html", "r").read(),
                        style={"width": "100%", "height": "500px", "border": "none"}
                    )
                ),
                dmc.Space(h="md"),
            ]
        ),

        dmc.Space(h="xl"),
        
        # ----------------------
        # Section : Carte interactive pour la prediction
        # ----------------------
        dmc.Card(
            shadow="sm",
            withBorder=True,
            padding="lg",
            className="scroll-section",
            children=[
                dmc.Title("More information about your town and estimated price per square meter for 2025", order=2),
                dmc.Space(h="md"),
                dmc.Paper(
                    style={
                        "height": "100vh",  # Prend toute la hauteur de la page
                        "width": "100%",    # Prend toute la largeur de la page
                        "display": "flex",  # Utilise Flexbox pour organiser les éléments
                        "flexDirection": "row",  # Disposition en ligne
                    },
                    children=[
                        # ----------------------
                        # Partie gauche : Choix de l'utilisateur
                        # ----------------------
                        dmc.Paper(
                            style={
                                "width": "20%",
                                "height": "85%",
                                "padding": "20px",
                                "boxSizing": "border-box",
                                "borderRight": "1px solid #ddd",
                                "overflowY": "auto",
                            },
                            children=[
                                html.H3("Estimate your property!", style={"marginTop": 0, "align": "center"}),
                                dmc.Space(h="md"),
                                html.P("Make your choices to get an estimate :"),
                                dmc.Select(
                                    label="Number of rooms",
                                    id="property-type",
                                    data=[
                                        {"label": "1 ROOM", "value": "1 ROOM"},
                                        {"label": "2 ROOM", "value": "2 ROOM"},
                                        {"label": "3 ROOM", "value": "3 ROOM"},
                                        {"label": "4 ROOM", "value": "4 ROOM"},
                                        {"label": "5 ROOM", "value": "5 ROOM"},
                                        {"label": "EXECUTIVE", "value": "EXECUTIVE"},
                                        {"label": "MULTI-GENERATION", "value": "MULTI-GENERATION"},
                                    ],
                                    placeholder="Select a flat_type",
                                    withScrollArea=False,
                                    mt="md",
                                ),
                                dmc.Space(h="md"),
                                html.Label("Area (m²) :"),
                                dmc.Slider(
                                    id="slider-callback",
                                    min=30,
                                    max=400,
                                    value=[30, 400],
                                    marks=[
                                        {"value": 30, "label": "30"},
                                        {"value": 100, "label": "100"},
                                        {"value": 200, "label": "200"},
                                        {"value": 300, "label": "300"},
                                        {"value": 400, "label": "400"},
                                    ],
                                    mb=35,
                                ),
                                dmc.Text(id="slider-output"),
                                dmc.Space(h="md"),
                                html.Label("Town :"),
                                dmc.Select(
                                    label="Town",
                                    id="quartier-select",
                                    data = [
                                        {"label": "Ang Mo Kio", "value": "Ang Mo Kio"},
                                        {"label": "Bedok", "value": "Bedok"},
                                        {"label": "Bishan", "value": "Bishan"},
                                        {"label": "Bukit Batok", "value": "Bukit Batok"},
                                        {"label": "Bukit Merah", "value": "Bukit Merah"},
                                        {"label": "Bukit Panjang", "value": "Bukit Panjang"},
                                        {"label": "Bukit Timah", "value": "Bukit Timah"},
                                        {"label": "Central Area", "value": "Central Area"},
                                        {"label": "Choa Chu Kang", "value": "Choa Chu Kang"},
                                        {"label": "Clementi", "value": "Clementi"},
                                        {"label": "Geylang", "value": "Geylang"},
                                        {"label": "Hougang", "value": "Hougang"},
                                        {"label": "Jurong East", "value": "Jurong East"},
                                        {"label": "Jurong West", "value": "Jurong West"},
                                        {"label": "Kallang/Whampoa", "value": "Kallang/Whampoa"},
                                        {"label": "Marine Parade", "value": "Marine Parade"},
                                        {"label": "Pasir Ris", "value": "Pasir Ris"},
                                        {"label": "Punggol", "value": "Punggol"},
                                        {"label": "Queenstown", "value": "Queenstown"},
                                        {"label": "Sembawang", "value": "Sembawang"},
                                        {"label": "Sengkang", "value": "Sengkang"},
                                        {"label": "Serangoon", "value": "Serangoon"},
                                        {"label": "Tampines", "value": "Tampines"},
                                        {"label": "Toa Payoh", "value": "Toa Payoh"},
                                        {"label": "Woodlands", "value": "Woodlands"},
                                        {"label": "Yishun", "value": "Yishun"},
                                    ],
                                    placeholder="Select a town",
                                    withScrollArea=True,
                                    mt="md",
                                ),
                                dmc.Space(h="md"),
                                dmc.Group(
                                    style={"display": "flex", "justifyContent": "center", "marginTop": "20px"},
                                    children=[
                                        dmc.Button("Estimate", id="estimate-btn", style={"marginTop": "10px"}, variant="default")
                                    ]
                                ),

                                dmc.Paper(style={"marginTop": "20px"}),

                                dmc.Text("Your estimate coming soon!", id="estimation-result", style={"fontSize": "18px", "fontWeight": "bold"}),
                            ],
                        ),
                        # ----------------------
                        # Partie centrale : Carte interactive
                        # ----------------------
                        dmc.Paper(
                            style={
                                "width": "40%",  # 50% de la largeur
                                "height": "85%",  # 85% de la hauteur
                            },
                            children=[
                                create_map(),  # Carte Leaflet
                            ],
                        ),
                        # ----------------------
                        # Partie droite : Graphiques avec SegmentedControl
                        # ----------------------
                        dmc.Paper(
                            style={
                                "width": "40%",
                                "height": "85%",
                                "padding": "20px",
                                "boxSizing": "border-box",
                                "borderLeft": "1px solid #ddd",
                                "overflowY": "auto",
                            },
                            children=[
                                dmc.SegmentedControl(
                                    id="graph-toggle",
                                    value="line-chart",  # Valeur par défaut
                                    data=[
                                        {"value": "line-chart", "label": "Price evolution"},
                                        {"value": "bar-chart", "label": "Average price"},
                                    ],
                                    fullWidth=True,
                                    style={"marginBottom": "20px"},
                                ),
                                dmc.Paper(
                                    id="line-chart-container",
                                    children=[dcc.Graph(id="price-trend-graph")],
                                    style={"display": "block"},  # Par défaut visible
                                ),
                                dmc.Paper(
                                    id="bar-chart-container",
                                    children=[dcc.Graph(id="price-bar-chart")],
                                    style={"display": "none"},  # Caché au début
                                ),
                                dcc.Store(id="selected-town", data="Ang Mo Kio"),
                                html.H3(id="town-name", children="Town : Ang Mo Kio"),
                            ],
                        ),

                        dmc.Space(h="md"),
                    ],
                    className="scroll-section",
                ),
            ]
        ),
        dmc.Space(h="xl"),
    ]
)


# Callback pour changer la carte affichée
@dash.callback(
    Output("map_iframe", "srcDoc"),
    Input("resale_or_pricem2", "value"),
)
def update_map(selected_value):
    if selected_value == "Resale":
        map_path = "services/maps/folium_map_resale.html"
    else:
        map_path = "services/maps/folium_map_price.html"

    with open(map_path, "r") as f:
        return f.read()
    

# Callback pour basculer entre les graphiques
@dash.callback(
    Output("graph-container", "children"),  # Mettre à jour le conteneur de graphiques
    Input("graph-toggle", "value"),  # Valeur sélectionnée dans le SegmentedControl
)
def update_graph(selected_graph):
    if selected_graph == "bar-chart":
        return dcc.Graph(id="price-per-sqm-bar-chart")
    elif selected_graph == "line-chart":
        return dcc.Graph(id="price-evolution-line-chart")
    return html.Div()  # Retourner un conteneur vide par défaut


@dash.callback(
    [
        Output("price-trend-graph", "figure"),
        Output("price-bar-chart", "figure"),
        Output("town-name", "children"),
        Output("selected-town", "data"),
        Output("line-chart-container", "style"),
        Output("bar-chart-container", "style"),
    ],
    [Input("geojson-layer", "n_clicks"), Input("graph-toggle", "value")],
    State("geojson-layer", "clickData")
)
def update_graph(n_clicks, graph_type, clickData):
    if not clickData or "properties" not in clickData:
        town_name = "Ang Mo Kio"
    else:
        town_name = clickData["properties"]["PLN_AREA_N"].title()

    # Générer les figures
    line_chart_fig = create_line_chart_figure_history_price(town_name)
    bar_chart_fig = create_bar_chart_figure(town_name)

    # Gérer l'affichage des graphiques
    if graph_type == "line-chart":
        line_chart_style = {"display": "block"}
        bar_chart_style = {"display": "none"}
    else:
        line_chart_style = {"display": "none"}
        bar_chart_style = {"display": "block"}

    return line_chart_fig, bar_chart_fig, f"Town : {town_name}", town_name, line_chart_style, bar_chart_style

@dash.callback(Output("slider-output", "children"), Input("slider-callback", "value"))
def update_value(value):
    return f"You have selected: {value}"

