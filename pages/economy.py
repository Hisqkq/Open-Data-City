import dash
import dash_mantine_components as dmc
import json
from dash import dcc, html, callback, Output, Input, State, ctx
from dash_extensions import Lottie
from dash_iconify import DashIconify

from figures.economy import create_unemployment_bar_chart, create_overal_unemployment_line, create_unemployment_residents_line_chart


dash.register_page(__name__, path="/economy")

layout = dmc.Container(
    fluid=True,
    p="xl",
    children=[

        html.Div(
            dmc.Title("Economic indicators", order=1, style={"marginBottom": "1rem", "textAlign": "center"}),
            style={"width": "100%"},
            className="scroll-section",
        ),
        
        # ---------- En-tête ----------
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
                            url="https://lottie.host/79d4e32b-2ed7-4df2-b4a5-b5ead10bc2be/yosMzk6470.json"
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
                dmc.Title("Unemployment rate by major cities", order=2),
                dmc.Space(h="md"),
                dmc.Text(
                    "This interactive line chart displays the evolution of student interest in various courses over the years. "
                    "By selecting a specific metric from the dropdown—such as intake, enrolment, graduates, or intake rate—you can examine "
                    "dynamic trends in course demand.",
                    size="md",
                    style={
                        "lineHeight": "1.6",
                        "textAlign": "justify"
                    }
                ),
                dmc.Space(h="md"),
                dcc.Graph(id="unemployment-rate-bar-chart"),
                dmc.Space(h="md"),
                dmc.Text(
                    "For instance, engineering studies are consistently among the most popular overall, and "
                    "especially among male students. In contrast, for female students, courses in Humanities & Social Sciences tend to lead in popularity."
                    "Moreover, when focusing on the intake rate (the percentage of admitted students relative to total enrolment), you’ll notice that "
                    "fields such as Architecture and Medicine register much lower rates. For example, Architecture typically appears at the bottom of "
                    "the intake rate rankings, with Medicine just above it. In the Dentistry field, there is also a marked difference between genders—men "
                    "exhibit an intake rate of approximately 34.5%, compared to around 21% for women. However, given the overall low number of students "
                    "in Dentistry, these percentage differences can be highly variable, and in some cases, women may even have a higher rate than men. "
                    "This chart provides nuanced insights into course competitiveness and helps to understand how demand shifts across disciplines over time.",
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

        # ---------- Section 2 :  ----------
        
        html.Div(
            children=[
                # Titre de la section
                html.Div(
                    dmc.Title("Evolution of Unemployment in Singapore", order=2, style={"textAlign": "center"}),
                    style={"width": "100%"}
                ),
                dmc.Space(h="xl"),
                dmc.Blockquote(
                    "Unemployed persons refer to people who are not working but are actively looking and available for jobs.",
                    cite="- Singapore Department of Statistics",
                    icon=DashIconify(icon="bx:bxs-quote-alt-right", height=20),
                    color="primary",
                    radius="lg",
                    style={"textAlign": "center", "width": "60%", "margin": "auto"}
                ),

                dmc.Space(h="lg"),
                
                # ---------- Section 1: Overall Unemployment (text + graph side by side) ----------
                html.Div(
                    style={
                        "display": "flex",
                        "flexWrap": "wrap",
                        "justifyContent": "center",
                        "alignItems": "center",
                        "gap": "1rem",
                        "width": "90%",
                        "margin": "auto"
                    },
                    children=[
                        # Texte explicatif à gauche
                        html.Div(
                            children=[
                                dmc.Group(
                                    children=[
                                        DashIconify(icon="tabler:chart-line", height=35),
                                        dmc.Title("Overall Trend", order=3, style={"margin": "0"})
                                    ],
                                ),
                                dmc.Text(
                                    "The graph on the right shows the overall unemployment rate in Singapore, including both residents and non-residents. "
                                    "This provides a broad perspective of the labor market dynamics over the years.",
                                    size="md",
                                    style={"lineHeight": "1.6", "textAlign": "justify"}
                                )
                            ],
                            style={"flex": "1"}
                        ),
                        # Graphique à droite
                        html.Div(
                            children=[
                                create_overal_unemployment_line()
                            ],
                            style={"flex": "2"}
                        )

                    ]
                ),
                dmc.Space(h="xl"),
                
                # ---------- Section 2: Residents Unemployment Trend with Selector ----------
                html.Div(
                    style={
                        "display": "flex",
                        "flexWrap": "wrap",
                        "justifyContent": "center",
                        "alignItems": "center",
                        "gap": "1rem",
                        "width": "90%",
                        "margin": "auto"
                    },
                    children=[
                        html.Div(
                            create_unemployment_residents_line_chart(),
                            id="unemployment-line-chart",
                            style={"flex": "2"}
                        ),
                        html.Div(
                            children=[
                                dmc.Group(
                                    children=[
                                        # house icon f
                                        DashIconify(icon="bx:bx-home", height=35),
                                        dmc.Title("Resident Unemployment Trends", order=3, style={"margin": "0"})
                                    ],
                                ),
                                dmc.Space(h="md"),
                                dmc.Text(
                                    "On the left is the unemployment trend for residents only. Use the dropdown to select the view mode: "
                                    "'By Highest Qualification', 'By Age', or 'By Sex'. This interactive tool allows you to dive deeper into the data, "
                                    "revealing differences across various groups.",
                                    size="md",
                                    style={"lineHeight": "1.6", "textAlign": "justify"}
                                ),
                                dmc.Select(
                                    id="unemployment-mode-select",
                                    value="Sex",
                                    data=[
                                        {"value": "Qualification", "label": "By Highest Qualification"},
                                        {"value": "Age", "label": "By Age"},
                                        {"value": "Sex", "label": "By Sex"}
                                    ],
                                    placeholder="Select view mode",
                                    style={"minWidth": "200px", "marginTop": "1rem", "width": "45%"}
                                ),
                            ],
                            style={"flex": "1"}
                            ),
                    ]
                ),
                dmc.Space(h="xl"),
            ]
        )

    ],
)


@callback(
    Output("unemployment-rate-bar-chart", "figure"),
    Input("theme-store", "data")
)
def update_unemployment_rate_bar_chart(theme):
    template = "mantine_dark" if theme == "dark" else "mantine_light"

    return create_unemployment_bar_chart(template)


@callback(
    Output("unemployment-line-chart", "children"),
    Input("unemployment-mode-select", "value")
)
def update_unemployment_line_chart(selected_mode):
    return create_unemployment_residents_line_chart(selected_mode),
        


