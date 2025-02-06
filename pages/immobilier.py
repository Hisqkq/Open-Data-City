import dash
import dash_mantine_components as dmc
import json
from dash import dcc, html, callback, Output, Input, State, ctx
from dash_extensions import Lottie
import plotly.express as px

from figures.immobilier_fig import create_line_chart_figure_introduction

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
                "alignItems": "top",
                "marginBottom": "1rem"
            },
            children=[
                html.Div(
                    style={"width": "75%"},
                    children=[
                        dmc.Title("Real estate in Singapore", order=1),
                        dmc.Text(
                            "Description à venir",
                            size="lg"
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
                                rendererSettings=dict(preserveAspectRatio='xMidYMid slice')
                            ),
                            width="100%",
                            url= "assets/img/Animation - 1738836928686.json"
                        )
                    ]
                ),
            ]
        ),
        dmc.Space(h="xl"),
        
        # ----------------------
        # Section : Graphique interactif
        # ----------------------
        html.Div(
            style={"position": "relative", "padding": "1rem"},
            children=[
                dmc.Title("Price per square metre over the last 8 years", order=3, style={"textAlign": "center"}),
                dmc.Space(h="md"),
                html.Button("Reset Graph", id="reset-btn", n_clicks=0, style={"position": "absolute", "top": "20px", "right": "20px"}),
                dcc.Graph(id="immo1-line-chart", figure=create_line_chart_figure_introduction()),
                dmc.Space(h="md")
            ]
        ),
        dmc.Space(h="xl"),
        
        # ----------------------
        # Section d'information complémentaire
        # ----------------------
        dmc.Card(
            shadow="sm",
            withBorder=True,
            padding="lg",
            children=[
                dmc.Title("About Real Estate Data", order=2),
                dmc.Text(
                    "Description incoming"
                )
            ]
        ),
        dmc.Space(h="xl"),
        
        # ----------------------
        # Section de débogage (à masquer en production)
        # ----------------------
        dmc.Card(
            shadow="sm",
            withBorder=True,
            padding="lg",
            children=[
                dmc.Title("Debug: clickData", order=4),
                html.Pre(id="clickdata-debug", style={"whiteSpace": "pre-wrap", "wordBreak": "break-word"})
            ]
        ),
        dmc.Space(h="xl"),
    ]
)