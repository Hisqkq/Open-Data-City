import dash
import dash_mantine_components as dmc
import json
from dash import dcc, html, callback, Output, Input, State, ctx
from dash_extensions import Lottie
import plotly.express as px

from figures.education import create_bar_chart_figure, create_line_chart_figure, create_admission_trends_figure

dash.register_page(__name__, path="/education")

layout = dmc.Container(
    fluid=True,
    p="xl",
    children=[
        # ---------- Stores pour suivre l'état interactif ----------
        dcc.Store(id="current-level", data="global"),
        dcc.Store(id="current-parent", data=None),

        html.Div(
            dmc.Title("Universities in Singapore", order=1, style={"marginBottom": "1rem", "textAlign": "center"}),
            style={"width": "100%"}
        ),
        
        # ---------- En-tête ----------
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
                        dmc.Text(
                            "Singapore is renowned for its highly competitive university admissions—a relentless pursuit of academic excellence that places enormous pressure on students and their families.",
                            size="lg"
                        ),
                        dmc.Space(h="sm"),
                        dmc.Text(
                            "This page provides a comprehensive analysis of education data, designed to guide prospective students, educators, and researchers in navigating these challenging dynamics. By examining overall admissions trends, course demand dynamics, institutional competitiveness, and graduate salary outcomes, we aim to shed light on how competition has evolved over the years and what it means for access to quality education.",
                            size="lg"
                        ),
                        dmc.Space(h="sm"),
                        dmc.Text(
                            "This in-depth exploration not only highlights the meritocratic drive behind Singapore's educational system but also raises critical questions about equity and sustainability in such a high-pressure setting. Through data-driven insights, we hope to empower stakeholders to make informed decisions and foster a more balanced academic environment, where success is measured by both achievement and opportunity.",
                            size="lg"
                        )
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
                            url="https://lottie.host/55f711be-705a-45f2-8f35-08456dcf6db0/8J4gG2IGrO.json"
                        )
                    ]
                ),
            ]
        ),
        dmc.Space(h="xl"),
        
        # ---------- Section 1 : Overall University Admissions Trends (Placeholder) ----------
        dmc.Card(
            shadow="sm",
            withBorder=True,
            padding="lg",
            children=[
                dmc.Title("Overall University Admissions Trends", order=2),
                dmc.Text(
                    "This chart will display the evolution of key university admission metrics—enrolment, intake, and admission rates—over the years. "
                    "It provides a global overview of the increasing competition for university places in Singapore.",
                    size="md"
                ),
                dcc.Graph(
                    id="admissions-trends-chart",
                )
            ]
        ),
        dmc.Space(h="xl"),
        
        # ---------- Section 2 : Course Demand Trends ----------
        dmc.Card(
            shadow="sm",
            withBorder=True,
            padding="lg",
            children=[
                dmc.Title("Course Demand Trends", order=2),
                dmc.Text(
                    "This interactive line chart shows the evolution of student interest in various courses over the years. "
                    "By selecting a specific metric (intake, enrolment, graduates, or intake rate) and filtering by gender (both, women, or men), "
                    "you can analyze which courses are experiencing increased demand and becoming more competitive.",
                    size="md"
                ),
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
                            checked=False  # Default mode: "closest"
                        ),
                        dmc.Button("Update Chart", id="update-chart-btn")
                    ]
                ),
                dmc.Space(h="md"),
                dcc.Graph(id="courses-line-chart")
            ]
        ),
        dmc.Space(h="xl"),
        
        # ---------- Section 3 : Institutional Trends (Placeholder) ----------
        dmc.Card(
            shadow="sm",
            withBorder=True,
            padding="lg",
            children=[
                dmc.Title("Institutional Trends", order=2),
                dmc.Text(
                    "This section will present a multi-line chart comparing selected institutions over the years. "
                    "A multi-select dropdown (coming soon) will allow you to choose several institutions, enabling you to compare how their metrics evolve and to gauge institutional competitiveness.",
                    size="md"
                ),
                dmc.Paper(
                    style={
                        "height": "300px",
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "center",
                        "backgroundColor": "#f1f3f5",
                        "border": "2px dashed #adb5bd"
                    },
                    children=dmc.Text("Institutional Trends Chart Coming Soon", size="xl", style={"textAlign": "center"})
                )
            ]
        ),
        dmc.Space(h="xl"),
        
        # ---------- Section 4 : Graduate Salary Outcomes (Bar Chart) ----------
        dmc.Card(
            shadow="sm",
            withBorder=True,
            padding="lg",
            style={"position": "relative"},
            children=[
                dmc.Title("Graduate Salary Outcomes", order=2, style={"textAlign": "center"}),
                html.Button("Reset Graph", id="reset-btn", n_clicks=0, style={"position": "absolute", "top": "20px", "right": "20px"}),
                dcc.Graph(
                    id="education-bar-chart",
                    figure=create_bar_chart_figure(detail_level="global", year=2022, template="mantine_light")
                ),
                dmc.Space(h="md"),
                dmc.Text(
                    "This bar chart presents the median gross salary of graduates by university. By clicking on a bar, you can drill down to see details at the school and degree level. "
                    "This detailed view helps illustrate the economic outcomes of different educational pathways.",
                    size="sm",
                    style={"textAlign": "center"}
                )
            ]
        ),
        dmc.Space(h="xl"),

    ]
)

@callback(
    Output("education-bar-chart", "figure"),
    Output("current-level", "data"),
    Output("current-parent", "data"),
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
    else:
        try:
            # Extraction du label cliqué dans l'axe x
            clicked_value = clickData["points"][0]["x"]
            
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
    
    return fig, new_level, new_parent

 

@callback(
    Output("courses-line-chart", "figure"),
    Input("metric-dropdown", "value"),
    Input("gender-dropdown", "value"),
    Input("theme-store", "data"),
    Input("hover-switch", "checked"),
)
def update_courses_line_chart(metric, gender, theme, hover_switch):
    template = "mantine_dark" if theme == "dark" else "mantine_light"
    hover_mode = "x unified" if hover_switch else "closest"

    if metric is None:
        metric = "intake"
    if gender is None:
        gender = "both"
    fig = create_line_chart_figure(metric=metric, gender=gender, template=template, hover_mode=hover_mode)
    return fig


@callback(
    Output("admissions-trends-chart", "figure"),
    Input("theme-store", "data")
)
def update_admissions_trends_chart(theme):
    template = "mantine_dark" if theme == "dark" else "mantine_light"
    fig = create_admission_trends_figure(template=template)
    return fig