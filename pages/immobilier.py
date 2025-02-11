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
        # Stores pour suivre le niveau et le parent courant
        dcc.Store(id="current-level", data="global"),
        dcc.Store(id="current-parent", data=None),
        
        # ----------------------
        # En-tête avec titre et animation Lottie
        # ----------------------
        html.Div(
            style={
                "display": "flex",
                "gap": "1rem",
                "alignItems": "center",
                "marginBottom": "2rem",
                "padding": "2rem",
                "background": "linear-gradient(135deg, #f5f7fa, #c3cfe2)",
                "borderRadius": "15px",
                "boxShadow": "0 4px 10px rgba(0, 0, 0, 0.1)",
            },
            children=[
                html.Div(
                    style={"width": "70%", "textAlign": "left"},
                    children=[
                        dmc.Title("Singapore and the Soaring Real Estate Market!", order=1, style={"color": "#2c3e50"}),
                        dmc.Text(
                            "Since 2017, Singapore’s property prices have seen a significant increase, reflecting the complex dynamics of the real estate market in one of the world’s most densely populated cities.",
                            size="lg",
                            style={"color": "#34495e"}
                        ),
                        dmc.Text(
                            "As the price per square meter continues to rise, the question arises: how does this trend impact housing affordability for residents?",
                            size="lg",
                            style={"color": "#34495e"}
                        ),
                        dmc.Text(
                            "Through this analysis, we will explore key figures, regional disparities, and future predictions to better understand the real estate challenges in Singapore.",
                            size="lg",
                            style={"color": "#34495e"}
                        ),
                    ]
                ),
                html.Div(
                    style={"width": "30%"},
                    children=[
                        Lottie(
                            options=dict(
                                loop=True,
                                autoplay=True,
                                rendererSettings=dict(preserveAspectRatio='xMidYMid slice')
                            ),
                            width="100%",
                            url="assets/img/Animation - 1738836928686.json"
                        )
                    ]
                ),
            ],
            className="fade-in",  # Ajouter une classe pour l'animation
        ),
        dmc.Space(h="xl"),
        
        # ----------------------
        # Section : Graphique interactif
        # ----------------------
        html.Div(
            style={
                "position": "relative",
                "padding": "2rem",
                "background": "#ffffff",
                "borderRadius": "15px",
                "boxShadow": "0 4px 10px rgba(0, 0, 0, 0.1)",
                "marginBottom": "2rem",
            },
            children=[
                dmc.Title("Price per Square Metre Over the Last 8 Years", order=3, style={"textAlign": "center", "color": "#2c3e50"}),
                dmc.Space(h="md"),
                html.Button(
                    "Reset Graph",
                    id="reset-btn",
                    n_clicks=0,
                    style={
                        "position": "absolute",
                        "top": "85px",
                        "right": "85px",
                        "background": "#3498db",
                        "color": "white",
                        "border": "none",
                        "padding": "10px 20px",
                        "borderRadius": "5px",
                        "cursor": "pointer",
                    }
                ),
                dcc.Graph(id="immo1-line-chart", figure=create_line_chart_figure_introduction()),
                dmc.Space(h="md")
            ],
            className="scroll-section",  # Ajouter une classe pour l'animation
        ),
        dmc.Space(h="xl"),

        # ----------------------
        # Section : Tableau Accroche
        # ----------------------
        html.Div(
            style={"position": "relative", "padding": "1rem"},
            children=[
                dmc.Title("Number of homes costing more than a million dollars at resale", order=3, style={"textAlign": "center"}),
                dmc.Space(h="md"),
                dcc.Graph(id="immo1-line-chart", figure=create_table_figure_introduction()),
                dmc.Space(h="md")
            ],
            className="scroll-section",
        ),
        dmc.Space(h="xl"),

        # ----------------------
        # Section : Carte interactive pour la prediction
        # ----------------------

        html.Div(
            style={
                "height": "100vh",
                "width": "100%",
                "display": "flex",
                "flexDirection": "row",
            },
            children=[
                # Section pour la carte (75% de la largeur)
                html.Div(
                    style={
                        "width": "66%",
                        "height": "85%",
                    },
                    children=[
                        # Carte Leaflet
                        create_map()
                    ],
                ),
            ],
            className="scroll-section",
        ),

        

        # ----------------------
        # Section : Carte interactive pour la prediction
        # ----------------------

        html.Div(
            style={
                "height": "100vh",
                "width": "100%",
                "display": "flex",
                "flexDirection": "row",
            },
            children=[
                # Section pour la carte (75% de la largeur)
                html.Div(
                    style={
                        "width": "66%",
                        "height": "85%",
                    },
                    children=[
                        # Carte Leaflet
                        create_map()
                    ],
                ),
                # Section pour la boîte d'informations (25% de la largeur)
                html.Div(
                    style={
                        "width": "34%",
                        "height": "85%",
                        "padding": "20px",
                        "boxSizing": "border-box",
                        "borderLeft": "1px solid #ddd",
                        "backgroundColor": "#f9f9f9",
                        "overflowY": "auto",
                    },
                    children=[
                        html.H3("Informations sur le quartier", style={"marginTop": 0}),
                        html.Div(
                            id="info-box-content",  # Contenu dynamique de la boîte
                            children="Cliquez sur un quartier pour afficher des informations.",
                        ),
                    ],
                ),
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