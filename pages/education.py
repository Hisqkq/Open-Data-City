import dash
import dash_mantine_components as dmc
import json
from dash import dcc, html, callback, Output, Input, ctx
from dash_extensions import Lottie
import plotly.express as px

from services.data.process_education_data import create_bar_chart_data
from figures.education import education_bar_chart

dash.register_page(__name__, path="/education")

layout = dmc.Container(
    fluid=True,
    p="xl",
    children=[
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
                        dmc.Title("Education in Singapore", order=1),
                        dmc.Text(
                            "Explore the diverse landscape of education in Singapore, from schools and universities to popular subjects and career outcomes. "
                            "Gain insights from interactive charts and detailed data analysis.",
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
                            url="https://lottie.host/55f711be-705a-45f2-8f35-08456dcf6db0/8J4gG2IGrO.json"
                        )
                    ]
                ),
            ]
        ),
        dmc.Space(h="xl"),
        
        # ----------------------
        # Section : Graphique interactif
        # ----------------------
        dmc.Card(
            shadow="sm",
            withBorder=True,
            padding="lg",
            style={"position": "relative"},
            children=[
                
                # Intégration du BarChart interactif
                dmc.Title("Graduate Employment Survey, per University, School and degree", order=3, style={"textAlign": "center"}),
                education_bar_chart(),
                dmc.Space(h="md"),
                dmc.Text("Click on a bar to drill down (e.g. view schools in the university).", size="sm", style={"textAlign": "center"})
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
                dmc.Title("About Education Data", order=2),
                dmc.Text(
                    "The Graduate Employment Survey gathers data from leading educational institutions in Singapore over the past decade. "
                    "This data helps prospective students compare universities, schools, and even specific degree programs based on graduate outcomes such as median gross salary. "
                    "Interact with the charts above to explore the data in more depth."
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
        
        # ... (vous pouvez ajouter d'autres sections ici)
    ]
)

@callback(
    Output("education-bar-chart", "data"),
    Output("education-bar-chart", "dataKey"),
    Output("education-bar-chart", "series"),
    Input("education-bar-chart", "clickData"),
    Input("reset-btn", "n_clicks")
)
def update_education_barchart(clickData, reset_n_clicks):
    """
    Met à jour le BarChart interactif de la page Education.
    
    - Si le bouton "Reset" est cliqué ou si aucun clic n'est détecté, on affiche la vue globale (agrégation par université).
    - Sinon, si un clic sur une barre est détecté, on passe au niveau de détail correspondant.
      * Si le clickData contient la clé "university", on affiche la vue 'university' (agrégation par école).
      * Si le clickData contient la clé "school", on affiche la vue 'school' (agrégation par degree).
    """
    triggered = ctx.triggered_id  # ID du composant déclencheur

    if triggered == "reset-btn" or clickData is None:
        result = create_bar_chart_data(detail_level="global", year=2022)
    else:
        try:
            if "university" in clickData:
                university = clickData["university"]
                result = create_bar_chart_data(detail_level="university", parent_value=university, year=2022)
            elif "school" in clickData:
                school = clickData["school"]
                result = create_bar_chart_data(detail_level="school", parent_value=school, year=2022)
            else:
                result = create_bar_chart_data(detail_level="global", year=2022)
        except Exception as e:
            result = create_bar_chart_data(detail_level="global", year=2022)
    
    return result["data"], result["dataKey"], result["series"]

@callback(
    Output("clickdata-debug", "children"),
    Input("education-bar-chart", "clickData")
)
def debug_clickdata(clickData):
    if clickData is None:
        return "No click detected."
    return json.dumps(clickData, indent=2, ensure_ascii=False)
