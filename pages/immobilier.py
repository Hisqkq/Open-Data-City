import dash
import dash_mantine_components as dmc
from dash import dcc, html
from dash_extensions import Lottie
import plotly.express as px
import dash_leaflet as dl
from dash import Output, Input, dcc, State
from dash_iconify import DashIconify
import pandas as pd
from figures.immobilier_fig import create_line_chart_figure_introduction, create_table_figure_introduction, create_line_chart_figure_history_price, create_bar_chart_figure
from services.maps.map_immo import create_map
from services.data.process_data_immo import process_town_street
from models.pred_immobilier import predict_immobilier

from utils.config import TOWNS

dash.register_page(__name__, path="/immobilier")

layout = dmc.Container(
    fluid=True,
    p="xl",
    children=[

         # Page Title
        html.Div(
            style={
                "width": "100%",
                "textAlign": "center",
                "margin": "auto",
                "marginTop": "1rem",
            },
            className="scroll-section",
            children=[
                dmc.Group(
                    children=[
                        DashIconify(icon="mdi:home", height=40, color="#228be6"),
                        dmc.Title("Real Estate Insights", order=1),
                    ],
                    align="center",
                    justify="center",
                    style={"margin": "auto", "textAlign": "center"}
                ),
                dmc.Text(
                    "Discover key trends and dynamics shaping Singapore's property market.",
                    size="md",
                    style={"marginTop": "0.5rem"}
                ),
                dmc.Space(h="xl"),
            ],
        ),

        # Main Section: Text & Animation side-by-side
        html.Div(
            style={
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "space-between",
                "gap": "1rem",
                "marginBottom": "2rem"
            },
            className="scroll-section",
            children=[
                # Left Column: Explanatory text and blockquote
                html.Div(
                    style={"flex": 1, "maxWidth": "65%"},
                    children=[
                        dmc.Blockquote(
                            "Real estate cannot be lost or stolen, nor can it be carried away. Purchased with common sense, paid for in full, and managed with reasonable care, it is about the safest investment in the world.",
                            cite="- Franklin D. Roosevelt",
                            icon=DashIconify(icon="mdi:lightbulb-on-outline", height=20, color="#228be6"),
                            color="primary",
                            radius="lg",
                            style={"textAlign": "center", "width": "100%"}
                        ),
                        dmc.Space(h="md"),
                        dmc.Text(
                            "Singapore's property market has experienced remarkable growth in recent years. This dashboard explores key metrics including "
                            "price per square meter, regional disparities, and market trends. Notably, central areas with high property values often have a "
                            "lower population density, while suburban regions reveal different dynamics. Understanding these nuances is essential for gauging "
                            "housing affordability and planning future developments.",
                            size="lg",
                            style={"lineHeight": "1.6", "textAlign": "justify"}
                        ),
                        dmc.Space(h="sm"),
                        dmc.Text(
                            "Through these insights, we aim to provide a comprehensive view of Singapore's real estate landscape, enabling informed decisions "
                            "for investors, policymakers, and residents.",
                            size="md",
                            style={"lineHeight": "1.6", "textAlign": "justify"}
                        ),
                    ]
                ),
                # Right Column: Animation
                html.Div(
                    style={"flex": 1, "maxWidth": "35%", "display": "flex", "justifyContent": "center"},
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
            ],
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


        # ---------- Section 2 :  ----------
        html.Div(
            className="scroll-section",
            children=[
                dmc.Title("Number of homes costing more than a million dollars at resale", order=2),
                dmc.Space(h="md"),

                # --- Première ligne : Table + Mini Card ---
                html.Div(
                    style={"display": "flex", "gap": "2rem", "justifyContent": "center", "alignItems": "stretch"},
                    children=[
                        # Table avec taille réduite et scroll si nécessaire
                        dmc.Card(
                            shadow="sm",
                            withBorder=True,
                            radius="md",
                            style={"flex": 1.5, "padding": "1rem", "maxWidth": "60%"},
                            children=[
                                dmc.Group(
                                    children=[
                                        DashIconify(icon="mdi:table-large", height=25, color="#228be6"),
                                        dmc.Title("Sales Overview", order=4),
                                    ]
                                ),
                                dmc.Space(h="sm"),
                                html.Div(
                                    create_table_figure_introduction(),
                                    style={"overflowX": "auto", "maxWidth": "100%"}  # Permet le scroll horizontal si besoin
                                )
                            ]
                        ),

                        # Mini Card avec du contenu supplémentaire pour équilibrer la hauteur
                        dmc.Card(
                            shadow="sm",
                            withBorder=True,
                            radius="md",
                            style={"flex": 1, "padding": "1rem"},
                            children=[
                                dmc.Group(
                                    children=[
                                        DashIconify(icon="mdi:trending-up", height=25, color="#ff5722"),
                                        dmc.Title("Explosive Growth", order=4),
                                    ]
                                ),
                                dmc.Space(h="sm"),
                                dcc.Markdown(
                                    """
                                    The number of **million-dollar resales** has **tripled** since 2021, reaching **940 sales in 2024**!  
                                    This surge reflects the **rapidly rising prices** in the real estate market. 


                                    This trend has several implications:
                                    - This could have implications for **housing affordability** and **social inequality**.
                                    - It could also indicate a **shift in consumer preferences** towards **luxury properties**.
                                    - Finally, it could be a sign of **speculative behavior** in the market.

                                    """,
                                    style={"lineHeight": "1.6", "textAlign": "justify", "fontSize": "16px"}
                                ),
                            ]
                        ),
                    ]
                ),

                dmc.Space(h="xl"),


                # --- Deuxième ligne : Deux Cards d'Analyse ---
                html.Div(
                    style={"display": "flex", "gap": "2rem", "justifyContent": "center", "alignItems": "start"},
                    children=[
                        # Card 1 - Evolution Analysis
                        dmc.Card(
                            shadow="sm",
                            withBorder=True,
                            radius="md",
                            style={"flex": 1, "padding": "1rem"},
                            children=[
                                dmc.Group(
                                    children=[
                                        DashIconify(icon="mdi:chart-line", height=25, color="#4caf50"),
                                        dmc.Title("Market Evolution", order=4),
                                    ]
                                ),
                                dmc.Space(h="sm"),
                                dcc.Markdown(
                                    """
                                    - **Before 2020**: Less than 100 properties exceeded S$1M.
                                    - **2021**: Sales tripled to **233 transactions**.
                                    - **2023**: The number doubled again to **426**.
                                    - **2024**: A record-breaking **940 sales**!
                                    """,
                                    style={"lineHeight": "1.6", "textAlign": "justify", "fontSize": "16px"}
                                ),
                            ]
                        ),

                        # Card 2 - Future Projections
                        dmc.Card(
                            shadow="sm",
                            withBorder=True,
                            radius="md",
                            style={"flex": 1, "padding": "1rem"},
                            children=[
                                dmc.Group(
                                    children=[
                                        DashIconify(icon="mdi:lightbulb-on-outline", height=25, color="#ff9800"),
                                        dmc.Title("What's Next?", order=4),
                                    ]
                                ),
                                dmc.Space(h="sm"),
                                dcc.Markdown(
                                    """
                                    - Already **120 sales** recorded in early 2025.
                                    - If this trend continues, **a new record is expected**.
                                    - Foreign investments and **rising demand** are fueling the growth.
                                    - Can this rapid rise **sustain itself** in the long run?
                                    """,
                                    style={"lineHeight": "1.6", "textAlign": "justify", "fontSize": "16px"}
                                ),
                            ]
                        ),
                    ]
                ),
            ],
            style={"margin": "auto", "padding": "1.5rem"}
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
                                    data = TOWNS,
                                    placeholder="Select a town",
                                    withScrollArea=True,
                                    mt="md",
                                ),
                                dmc.Space(h="md"),
                                dmc.Select(
                                    label="Street",
                                    id="street-select",
                                    data=[],  # Commence avec une liste vide
                                    placeholder="Select a street",
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

                                dmc.Text( id="estimation-result", style={"fontSize": "18px", "fontWeight": "bold"}),
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


@dash.callback(
    Output("street-select", "data"), 
    Input("quartier-select", "value"),
)
def update_street_dropdown(selected_town):
    if not selected_town:
        return []
    streets = process_town_street().get(selected_town, [])
    return [{"label": street, "value": street} for street in streets]

@dash.callback(
    Output("estimation-result", "children"),
    Input("estimate-btn", "n_clicks"),
    State("property-type", "value"),
    State("quartier-select", "value"),
    State("street-select", "value"),
    State("slider-callback", "value"),
)
def estimate_price(n_clicks, flat_type, town, street_name, floor_area_sqm):
    if not n_clicks:
        return "Your estimate coming soon!"

    # Vérifier si toutes les entrées nécessaires sont remplies
    if not all([flat_type, town, street_name, floor_area_sqm]):
        return "Please select all required fields."

    # Construire la dataframe pour la prédiction
    input_data = pd.DataFrame([{
        "month": 1,  # Janvier par défaut
        "year": 2025,  # Année suivante
        "town": town,
        "flat_type": flat_type,
        "street_name": street_name,
        "storey_range": "04 TO 06",  # Valeur par défaut
        "floor_area_sqm": floor_area_sqm,
        "flat_model": "Apartment",  # Valeur par défaut
        "lease_commence_date": 2000,  # Valeur par défaut
        "remaining_lease_years": 6.5  # Valeur par défaut
    }])

    # Faire la prédiction
    predicted_price = predict_immobilier(input_data)

    # Retourner le résultat formaté
    return f"Estimated Price: {predicted_price[0]:,.2f} SGD"