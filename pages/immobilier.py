import dash
import dash_mantine_components as dmc
import json
from dash import dcc, html, callback, Output, Input, State, ctx
from dash_extensions import Lottie
import plotly.express as px

from figures.immobilier_fig import create_line_chart_figure_introduction, create_table_figure_introduction

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
                        dmc.Title("Singapore and the soaring real estate market!", order=1),
                        dmc.Text("Since 2017, Singapore’s property prices have seen a significant increase, reflecting the complex dynamics of the real estate market in one of the world’s most densely populated cities.", size="lg"),
                        dmc.Text("As the price per square meter continues to rise, the question arises: how does this trend impact housing affordability for residents?", size="lg"),
                        dmc.Text("Through this analysis, we will explore key figures, regional disparities, and future predictions to better understand the real estate challenges in Singapore.", size="lg")
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
        # Section : Graphique Accroche
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
        # Section : Tableau Accroche
        # ----------------------
        html.Div(
            style={"position": "relative", "padding": "1rem"},
            children=[
                dmc.Title("Number of homes costing more than a million dollars at resale", order=3, style={"textAlign": "center"}),
                dmc.Space(h="md"),
                dcc.Graph(id="immo1-line-chart", figure=create_table_figure_introduction()),
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