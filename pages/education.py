import dash
import dash_mantine_components as dmc
import json
from dash import dcc, html, callback, Output, Input, State, ctx
from dash_extensions import Lottie
import plotly.express as px

from figures.education import create_bar_chart_figure, create_line_chart_figure

dash.register_page(__name__, path="/education")

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
        html.Div(
            style={"position": "relative", "padding": "1rem"},
            children=[
                dmc.Title("Graduate Employment Survey, per University, School and Degree", order=3, style={"textAlign": "center"}),
                dmc.Space(h="md"),
                html.Button("Reset Graph", id="reset-btn", n_clicks=0, style={"position": "absolute", "top": "20px", "right": "20px"}),
                dcc.Graph(id="education-bar-chart", figure=create_bar_chart_figure(detail_level="global", year=2022, template="mantine_light")),
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

        # ----------------------

        dmc.Title("Courses Evolution", order=1),
        dmc.Text("Select a metric and gender to see the evolution of courses over the years."),
        dmc.Group(
            children=[
                dmc.Select(
                    id="metric-dropdown",
                    data=[
                        {"value": "intake", "label": "Intake"},
                        {"value": "enrolment", "label": "Enrolment"},
                        {"value": "graduates", "label": "Graduates"},
                        {"value": "intake_rate", "label": "Intake Rate"}
                    ],
                    placeholder="Select a metric"
                ),
                dmc.Select(
                    id="gender-dropdown",
                    data=[
                        {"value": "both", "label": "Both"},
                        {"value": "women", "label": "Women"},
                        {"value": "men", "label": "Men"}
                    ],
                    placeholder="Select a gender"
                ),
                dmc.Switch(
                    id="hover-switch",
                    label="Year-by-year hover",
                    checked=False  # par défaut : mode 'closest'
                ),
            ]
        ),
        dmc.Space(h="md"),
        dcc.Graph(id="courses-line-chart"),
    ]
)

@callback(
    Output("education-bar-chart", "figure"),
    Output("current-level", "data"),
    Output("current-parent", "data"),
    Output("clickdata-debug", "children"),
    Input("education-bar-chart", "clickData"),
    Input("reset-btn", "n_clicks"),
    Input("theme-store", "data"),
    State("current-level", "data"),
    State("current-parent", "data")
)
def update_education_chart(clickData, reset_n_clicks, theme, current_level, current_parent):
    # Détermine le template en fonction du thème
    template = "mantine_dark" if theme == "dark" else "mantine_light"
    triggered = ctx.triggered_id
    debug_info = ""
    
    # Si le bouton Reset a été cliqué ou qu'aucun clic n'est détecté,
    # on réinitialise le graphique en vue globale et on vide le parent.
    if triggered == "reset-btn" or clickData is None or triggered == "theme-store":
        new_level = "global"
        new_parent = None
        fig = create_bar_chart_figure(detail_level="global", year=2022, template=template)
        debug_info = "Reset to global view."
    else:
        try:
            # Extraction du label cliqué dans l'axe x
            clicked_value = clickData["points"][0]["x"]
            debug_info = json.dumps(clickData, indent=2, ensure_ascii=False)
            
            if current_level == "global":
                new_level = "university"
                new_parent = clicked_value  # le parent est le nom de l'université
                fig = create_bar_chart_figure(detail_level="university", parent_value=clicked_value, year=2022, template=template)
            elif current_level == "university":
                new_level = "school"
                new_parent = clicked_value  # le parent est le nom de l'école
                fig = create_bar_chart_figure(detail_level="school", parent_value=clicked_value, year=2022, template=template)
            elif current_level == "school":
                # Si on est déjà au niveau le plus profond, on réinitialise vers global.
                new_level = "global"
                new_parent = None
                fig = create_bar_chart_figure(detail_level="global", year=2022, template=template)
            else:
                new_level = "global"
                new_parent = None
                fig = create_bar_chart_figure(detail_level="global", year=2022, template=template)
        except Exception as e:
            new_level = "global"
            new_parent = None
            fig = create_bar_chart_figure(detail_level="global", year=2022, template=template)
            debug_info = f"Erreur: {e}. Retour à la vue globale."
    
    return fig, new_level, new_parent, debug_info

 

@callback(
    Output("courses-line-chart", "figure"),
    Input("metric-dropdown", "value"),
    Input("gender-dropdown", "value"),
    Input("theme-store", "data"),
    Input("hover-switch", "checked"),
)
def update_courses_line_chart(metric, gender, theme, hover_switch):
    # Choix du template Plotly en fonction du switch
    template = "mantine_dark" if theme == "dark" else "mantine_light"
    hover_mode = "x unified" if hover_switch else "closest"

    # Valeurs par défaut
    if metric is None:
        metric = "intake"
    if gender is None:
        gender = "both"
    fig = create_line_chart_figure(metric=metric, gender=gender, template=template, hover_mode=hover_mode)
    return fig