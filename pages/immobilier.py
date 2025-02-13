import dash
import dash_mantine_components as dmc
from dash import dcc, html
from dash_extensions import Lottie
import plotly.express as px
import dash_leaflet as dl
from dash import Output, Input, dcc
import pandas as pd
from figures.immobilier_fig import create_line_chart_figure_introduction, create_table_figure_introduction
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
        html.Div(
            style={
                "display": "flex",
                "gap": "1rem",
                "alignItems": "top",
                "marginBottom": "1rem"
            },
            className="scroll-section",
            children=[
                html.Div(
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

                html.Div(
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
                dcc.Graph(id="immo1-line-chart", figure=create_line_chart_figure_introduction()),
                dmc.Space(h="md"),
                dmc.Text(
                    """
                    The graph illustrates the evolution of the price per square meter over the last eight years. Three distinct phases can be observed.
                    Between 2017 and mid-2020, prices remained relatively stable, fluctuating between €4,500 and €4,700/m², without significant variation.
                    This period of stagnation seems to mark a balance between supply and demand.

                    From mid-2020 to 2021, a major turning point occurred. Prices began to rise dramatically, quickly exceeding €5,000/m²
                    in just a few months. This sudden increase coincided with the end of the health crisis, marking a new dynamic in the real estate market.

                    From 2022 to today, the upward trend has not slowed down. On the contrary, prices continue to accelerate, reaching more than €7,000/m² in 2025,
                    a historic record that reflects strong pressure on the market.

                    Several factors can explain this surge in prices. First, the post-COVID period has led to an economic recovery and changes in
                    purchasing habits, with increased demand for certain types of properties. Then, inflation and rising construction costs have
                    had a strong impact on the price of new projects, limiting supply and fueling price increases. Finally, the growing attractiveness of certain areas
                    has led to an influx of buyers, further increasing pressure on the market.

                    The question remains: will this trend continue, or are we on the verge of a market turnaround? Only time will tell.
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
                html.Div(create_table_figure_introduction(), id="immo1-table-container"),
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
        
        # ----------------------
        # Section : Carte interactive pour la prediction
        # ----------------------

        html.Div(
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
                html.Div(
                    style={
                        "width": "20%",
                        "height": "85%",
                        "padding": "20px",
                        "boxSizing": "border-box",
                        "borderRight": "1px solid #ddd",
                        "backgroundColor": "#f9f9f9",
                        "overflowY": "auto",
                    },
                    children=[
                        html.H3("Estimation de bien", style={"marginTop": 0}),
                        html.P("Faites vos choix pour obtenir une estimation :"),
                        # Exemple de filtres (à adapter)
                        html.Label("Type de bien :"),
                        dcc.Dropdown(
                            id="property-type",
                            options=[
                                {"label": "Appartement", "value": "apartment"},
                                {"label": "Maison", "value": "house"},
                            ],
                            placeholder="Sélectionnez un type de bien",
                        ),
                        html.Label("Surface (m²) :"),
                        dcc.Input(id="surface", type="number", placeholder="Entrez la surface"),
                        html.Label("Quartier :"),
                        dcc.Dropdown(
                            id="quartier-select",
                            # options=[{"label": q, "value": q} for q in df["Quartier"].unique()],
                            placeholder="Sélectionnez un quartier",
                        ),
                        html.Button("Estimer", id="estimate-btn", style={"marginTop": "10px"}),
                    ],
                ),
                # ----------------------
                # Partie centrale : Carte interactive
                # ----------------------
                html.Div(
                    style={
                        "width": "50%",  # 50% de la largeur
                        "height": "85%",  # 85% de la hauteur
                    },
                    children=[
                        create_map(),  # Carte Leaflet
                    ],
                ),
                # ----------------------
                # Partie droite : Graphiques
                # ----------------------
        # ----------------------
        # Partie droite : Graphiques avec SegmentedControl
        # ----------------------
                html.Div(
                    style={
                        "width": "25%",  # 25% de la largeur
                        "height": "85%",  # 85% de la hauteur
                        "padding": "20px",
                        "boxSizing": "border-box",
                        "borderLeft": "1px solid #ddd",
                        "backgroundColor": "#ffffff",
                        "overflowY": "auto",
                    },
                    children=[
                        # SegmentedControl pour basculer entre les graphiques
                        dmc.SegmentedControl(
                            id="graph-toggle",
                            value="bar-chart",  # Valeur par défaut
                            data=[
                                {"value": "bar-chart", "label": "Prix au m²"},
                                {"value": "line-chart", "label": "Évolution des prix"},
                            ],
                            fullWidth=True,
                            style={"marginBottom": "20px"},
                        ),
                        # Conteneur pour les graphiques
                        html.Div(
                            id="graph-container",
                            children=[
                                # Bar chart par défaut
                                dcc.Graph(id="price-per-sqm-bar-chart"),
                            ],
                        ),
                    ],
                ),
                dmc.Space(h="md"),
            ],
            className="scroll-section",
        ),

        # ----------------------
        # Section d'information complémentaire
        # ----------------------
        dmc.Card(
            shadow="sm",
            withBorder=True,
            padding="lg",
            style={
                "background": "#ffffff",
                "borderRadius": "15px",
                "boxShadow": "0 4px 10px rgba(0, 0, 0, 0.1)",
                "marginBottom": "2rem",
            },
            children=[
                dmc.Title("About Real Estate Data", order=2, style={"color": "#2c3e50"}),
                dmc.Text(
                    "Description incoming",
                    size="lg",
                    style={"color": "#34495e"}
                )
            ],
            className="scroll-section",  # Ajouter une classe pour l'animation
        ),
        dmc.Space(h="xl"),
        
        # ----------------------
        # Section de débogage (à masquer en production)
        # ----------------------
        dmc.Card(
            shadow="sm",
            withBorder=True,
            padding="lg",
            style={
                "background": "#ffffff",
                "borderRadius": "15px",
                "boxShadow": "0 4px 10px rgba(0, 0, 0, 0.1)",
            },
            children=[
                dmc.Title("Debug: Click Data", order=4, style={"color": "#2c3e50"}),
                html.Pre(
                    id="clickdata-debug",
                    style={"whiteSpace": "pre-wrap", "wordBreak": "break-word", "color": "#34495e"}
                )
            ],
            className="scroll-section",  # Ajouter une classe pour l'animation
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