import dash
import dash_mantine_components as dmc
import json
from dash import dcc, html, callback, Output, Input, State, ctx
from dash_extensions import Lottie
import plotly.express as px
from dash_iconify import DashIconify

from figures.education import create_bar_chart_figure, create_line_chart_figure, create_admission_trends_figure, create_institution_trends_figure, create_corr_institution_figure

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
                            url="https://lottie.host/55f711be-705a-45f2-8f35-08456dcf6db0/8J4gG2IGrO.json"
                        )
                    ]
                ),
            ]
        ),
        dmc.Space(h="xl"),
        
        # ---------- Section 1 : Overall University Admissions Trends ----------
        dmc.Card(
            shadow="sm",
            withBorder=True,
            padding="lg",
            className="scroll-section",
            style={
                "borderRadius": "10px",
                "padding": "2rem"
            },
            children=[
                dmc.Title("Overall University Admissions Trends", order=2, style={"textAlign": "center"}),
                dmc.Space(h="md"),
                dmc.Text(
                    "This comprehensive chart displays the evolution of key university admission metrics – including total enrolment, intake numbers, and overall admission rates – over the past two decades. "
                    "It vividly illustrates the rapid growth in university applications while highlighting the increasing competition for limited places. "
                    "Notably, the intake rate has dropped by approximately 2% since 2005, reaching as low as 22.5% in 2022. This decline underscores the mounting pressure on prospective students to secure admission.",
                    size="md",
                    style={
                        "lineHeight": "1.6",
                        "textAlign": "justify",
                        "marginBottom": "1rem"
                    }
                ),
                dmc.Switch(
                            id="education-prediction-switch",
                            label="Show Predictions",
                            checked=True
                        ),
                dmc.Space(h="md"),
                dcc.Graph(
                    id="admissions-trends-chart",
                ),
                dmc.Space(h="md"),
                dmc.Text(
                    "These trends not only reflect the soaring number of applications but also signal a tightening admission process, making competition fiercer than ever. "
                    "Up next, we will explore which fields of study are the most competitive, shedding light on course demand dynamics and access challenges at a more granular level.",
                    size="md",
                    style={
                        "lineHeight": "1.6",
                        "textAlign": "justify"
                    }
                ),
                dmc.Space(h="md"),
                dmc.Accordion(
                    disableChevronRotation=True,
                    children=[
                        dmc.AccordionItem(
                            [
                                dmc.AccordionControl(
                                    "How were the predictions made?",
                                    icon=DashIconify(
                                        icon="mdi:information-outline",
                                        color=dmc.DEFAULT_THEME["colors"]["blue"][6],
                                        width=20,
                                    ),
                                ),
                                dmc.AccordionPanel(
                                    [
                                        dmc.Text("Prediction Methodology:", size="lg", style={"marginBottom": "10px"}),
                                        dmc.Text(
                                            "To forecast future university admissions, we employed a Quantile Regression model combined with a Box-Cox transformation. "
                                            "This approach was chosen to handle non-linear relationships and to stabilize variance in our data.",
                                            style={"marginBottom": "10px"}
                                        ),
                                        dmc.Text("Box-Cox Transformation:", size="lg", style={"marginBottom": "10px"}),
                                        dmc.Text(
                                            "The Box-Cox transformation is a power transformation that aims to make data more normally distributed. "
                                            "By applying this transformation to our 'intake' and 'enrolment' variables, we achieved a more linear relationship, "
                                            "which is essential for regression analysis.",
                                            style={"marginBottom": "10px"}
                                        ),
                                        dmc.Text("Quantile Regression:", size="lg", style={"marginBottom": "10px"}),
                                        dmc.Text(
                                            "Unlike traditional regression models that predict the mean of the dependent variable, Quantile Regression predicts specific quantiles (e.g., the median). "
                                            "This is particularly useful for understanding the distributional effects and is robust to outliers.",
                                            style={"marginBottom": "10px"}
                                        ),
                                        dmc.Text("Implementation Steps:", size="lg", style={"marginBottom": "10px"}),
                                        dmc.List(
                                            [
                                                dmc.ListItem(
                                                    dmc.Text(
                                                        "Data Transformation: Applied the Box-Cox transformation to the 'intake' and 'enrolment' data to stabilize variance and achieve normality.",
                                                        style={"marginBottom": "5px"}
                                                    )
                                                ),
                                                dmc.ListItem(
                                                    dmc.Text(
                                                        "Model Training: Trained Quantile Regression models (at the 0.5 quantile) using the transformed data to capture the median relationship between the variables and time.",
                                                        style={"marginBottom": "5px"}
                                                    )
                                                ),
                                                dmc.ListItem(
                                                    dmc.Text(
                                                        "Prediction: Used the trained models to predict future values for 'intake' and 'enrolment' up to the year 2028.",
                                                        style={"marginBottom": "5px"}
                                                    )
                                                ),
                                                dmc.ListItem(
                                                    dmc.Text(
                                                        "Inverse Transformation: Applied the inverse Box-Cox transformation to the predicted values to revert them to the original scale.",
                                                        style={"marginBottom": "5px"}
                                                    )
                                                ),
                                            ],
                                            style={"marginBottom": "10px"}
                                        ),
                                        dmc.Text("Rationale for Choices:", size="lg", style={"marginBottom": "10px"}),
                                        dmc.Text(
                                            "The combination of Box-Cox transformation and Quantile Regression allows for flexibility in modeling non-linear relationships and provides robustness against outliers. "
                                            "This methodology ensures that our predictions are not unduly influenced by extreme values and that they capture the central tendency of the data over time.",
                                            style={"marginBottom": "10px"}
                                        ),
                                    ]
                                ),
                            ],
                            value="info",
                            style={"marginBottom": "1rem", "width": "80%", "textAlign": "justify", "margin": "auto"},
                        ),
                    ],
                ),
            ]
        ),
        dmc.Space(h="xl"),

        
        # ---------- Section 2 : Course Demand Trends ----------
        dmc.Card(
            shadow="sm",
            withBorder=True,
            padding="lg",
            className="scroll-section",
            children=[
                dmc.Title("Course Demand Trends", order=2),
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
                            placeholder="Select a metric",
                            label="Metric"
                        ),
                        dmc.Select(
                            id="gender-dropdown",
                            data=[
                                {"value": "both", "label": "Both"},
                                {"value": "women", "label": "Women"},
                                {"value": "men", "label": "Men"}
                            ],
                            placeholder="Select a gender",
                            label="Gender"
                        ),
                        dmc.Switch(
                            id="hover-switch",
                            label="Year-by-year hover",
                            checked=False  # Default mode: "closest"
                        )
                    ]
                ),
                dmc.Space(h="md"),
                dcc.Graph(id="courses-line-chart"),
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

        
        # ---------- Section 3: Institutional Trends (Placeholder) ----------
        dmc.Card(
            shadow="sm",
            withBorder=True,
            padding="lg",
            className="scroll-section",
            children=[
                dmc.Title("Institutional Trends", order=2),
                dmc.Space(h="md"),
                # Texte explicatif au-dessus de la figure
                dmc.Text(
                    "Overview: This section presents an interactive multi-line chart that compares the evolution of key admission metrics over the years across various higher education institutions. "
                    "By using the multi-select dropdown, you can choose one or more institutions to compare their trends. The chart displays metrics such as enrolment, intake, and intake rate side by side, "
                    "allowing you to explore differences in institutional competitiveness. For example, while universities dominate the scene, the dropdown also enables comparisons with other types of "
                    "higher education providers.",
                    size="md",
                    style={
                        "lineHeight": "1.6",
                        "textAlign": "justify",
                        "marginBottom": "1rem"
                    }
                ),
                dmc.Space(h="md"),
                dcc.Graph(
                    id="institution-trends-chart",
                ),
                dmc.Group(
                    children=[
                        dmc.MultiSelect(
                            id="institution-multiselect",
                            value=["ntu", "nus", "smu", "sutd", "suss"],
                            data=[
                                {"value": "ite", "label": "ITE"},
                                {"value": "lasalle_degree", "label": "La Salle Degree"},
                                {"value": "lasalle_diploma", "label": "La Salle Diploma"},
                                {"value": "nafa_degree", "label": "NAFA Degree"},
                                {"value": "nafa_diploma", "label": "NAFA Diploma"},
                                {"value": "nanyang_polytechnic", "label": "Nanyang Polytechnic"},
                                {"value": "ngee_ann_polytechnic", "label": "NGEE Ann Polytechnic"},
                                {"value": "nie", "label": "NIE"},
                                {"value": "ntu", "label": "NTU"},
                                {"value": "nus", "label": "NUS"},
                                {"value": "republic_polytechnic", "label": "Republic Polytechnic"},
                                {"value": "singapore_polytechnic", "label": "Singapore Polytechnic"},
                                {"value": "sit", "label": "SIT"},
                                {"value": "smu", "label": "SMU"},
                                {"value": "suss", "label": "SUSS"},
                                {"value": "sutd", "label": "SUTD"},
                                {"value": "temasek_polytechnic", "label": "Temasek Polytechnic"}
                            ],
                            placeholder="Select institutions",
                            label="Institutions"
                        ),
                        dmc.Select(
                            id="institution-metric-dropdown",
                            data=[
                                {"value": "enrolment", "label": "Enrolment"},
                                {"value": "intake", "label": "Intake"},
                                {"value": "intake_rate", "label": "Intake Rate"}
                            ],
                            placeholder="Select a metric",
                            label="Metric"
                        )
                    ]
                ),
                dmc.Space(h="md"),
                # Texte d'observations en dessous de la figure
                html.Div(
                        children=[
                            dmc.Text(
                                "Observations: Preliminary data indicates that among the institutions, NUS is the most popular, followed closely by NTU. "
                                "In general, university intake rates tend to range between 24% and 28%. Moreover, when a new institution is established, its initial admission rate is exceptionally high, "
                                "but this rate declines rapidly and stabilizes over time. These trends highlight the competitive landscape of higher education in Singapore and offer valuable insights into how "
                                "admission strategies evolve over the years.",
                                size="md",
                                style={
                                    "lineHeight": "1.6",
                                    "marginTop": "1rem",
                                    "flex": "1"
                                }
                            ),
                            dcc.Graph(id="corr-institution-chart", style={"marginTop": "1rem", "flex": "2"}, config={'displayModeBar': False}),
                    ],
                style={"display": "flex",
                        "flexWrap": "wrap",
                        "justifyContent": "center",
                        "alignItems": "center",
                        "gap": "1rem",
                        "width": "90%",
                        "margin": "auto"}
            )
            ]
        ),
        dmc.Space(h="xl"),

        
        # ---------- Section 4 : Graduate Salary Outcomes (Bar Chart) ----------
        dmc.Card(
            shadow="sm",
            withBorder=True,
            padding="lg",
            className="scroll-section",
            style={"position": "relative"},
            children=[
                # Titre de la section
                dmc.Title("Graduate Salary Outcomes", order=2, style={"textAlign": "center"}),
                dmc.Space(h="md"),
                # Texte explicatif au-dessus du graphique
                dmc.Text(
                    "While gaining admission to Singapore's universities is extremely competitive, the outcomes in terms of graduate salaries and employment rates reveal further insights into the system. "
                    "Based on 2022 data, the chart below illustrates the median gross salaries across universities. Notice that these bars are colored according to the employment rate, "
                    "providing an additional perspective on how easy or challenging it is to secure a job after graduation.",
                    size="md",
                    style={
                        "lineHeight": "1.6",
                        "textAlign": "justify",
                        "marginBottom": "1rem"
                    }
                ),
                # Bouton Reset positionné en haut à droite
                html.Button(
                    "Reset Graph",
                    id="reset-btn",
                    n_clicks=0,
                    style={"position": "absolute", "top": "20px", "right": "20px"}
                ),
                # Graphique interactif
                dcc.Graph(
                    id="education-bar-chart",
                    figure=create_bar_chart_figure(detail_level="global", year=2022, template="mantine_light")
                ),
                dmc.Space(h="md"),
                # Texte explicatif en dessous du graphique
                dmc.Text(
                    "By clicking on a bar, you can drill down into more detailed views: first by university, then by school, and finally by degree. "
                    "This interactive functionality allows you to uncover which educational pathways yield the highest starting salaries. "
                    "For instance, programs in Law, Medicine, and Engineering typically offer higher salaries upon graduation, while courses in the social sciences, such as early childhood education, tend to pay less. "
                    "The color of each bar represents the employment rate for that category, offering insights into post-graduation job prospects.",
                    size="md",
                    style={
                        "lineHeight": "1.6",
                        "textAlign": "justify",
                        "marginTop": "1rem"
                    }
                )
            ]
        ),
        dmc.Space(h="xl"),

        html.Div(
            children=[
                dmc.Title("References", order=3, style={"textAlign": "center", "marginBottom": "1rem"}),
                
                dmc.Text(
                    "Ministry of Education. (2022). Graduate Employment Survey - NTU, NUS, SIT, SMU, SUSS & SUTD (2024) [Dataset]. "
                    "data.gov.sg. Retrieved February 8, 2025 from ",
                    size="xs",
                    style={"textAlign": "center"}
                ),
                dmc.Anchor(
                    "https://data.gov.sg/datasets/d_3c55210de27fcccda2ed0c63fdd2b352/view",
                    href="https://data.gov.sg/datasets/d_3c55210de27fcccda2ed0c63fdd2b352/view",
                    target="_blank",
                    size="xs",
                    style={"textAlign": "center"}
                ),
                dmc.Space(h="sm"),
                
                dmc.Text(
                    "Ministry of Education. (2019). Intake, Enrolment and Graduates of Universities by Course (2024) [Dataset]. "
                    "data.gov.sg. Retrieved February 8, 2025 from ",
                    size="xs",
                    style={"textAlign": "center"}
                ),
                dmc.Anchor(
                    "https://data.gov.sg/datasets/d_6b264092cd066c55d8e2db9e68e7ffdb/view",
                    href="https://data.gov.sg/datasets/d_6b264092cd066c55d8e2db9e68e7ffdb/view",
                    target="_blank",
                    size="xs",
                    style={"textAlign": "center"}
                ),
                dmc.Space(h="sm"),
                
                dmc.Text(
                    "Ministry of Education. (2019). Enrolment by Institutions (2024) [Dataset]. "
                    "data.gov.sg. Retrieved February 8, 2025 from ",
                    size="xs",
                    style={"textAlign": "center"}
                ),
                dmc.Anchor(
                    "https://data.gov.sg/datasets/d_ec8a16e11a050f11880fb6d4a0e6f93f/view",
                    href="https://data.gov.sg/datasets/d_ec8a16e11a050f11880fb6d4a0e6f93f/view",
                    target="_blank",
                    size="xs",
                    style={"textAlign": "center"}
                ),
                dmc.Space(h="sm"),
                
                dmc.Text(
                    "Ministry of Education. (2019). Intake by Institutions (2024) [Dataset]. "
                    "data.gov.sg. Retrieved February 8, 2025 from ",
                    size="xs",
                    style={"textAlign": "center"}
                ),
                dmc.Anchor(
                    "https://data.gov.sg/datasets/d_437e089ba21c5221b0d42e3b2636b7f0/view",
                    href="https://data.gov.sg/datasets/d_437e089ba21c5221b0d42e3b2636b7f0/view",
                    target="_blank",
                    size="xs",
                    style={"textAlign": "center"}
                )
            ],
            style={"marginTop": "2rem", "textAlign": "center"}
        )

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
    Input("theme-store", "data"),
    Input("education-prediction-switch", "checked")
)
def update_admissions_trends_chart(theme, show_predictions):
    template = "mantine_dark" if theme == "dark" else "mantine_light"
    fig = create_admission_trends_figure(template=template, show_regression=show_predictions)
    return fig


@callback(
    Output("institution-trends-chart", "figure"),
    Input("institution-multiselect", "value"),
    Input("institution-metric-dropdown", "value"),
    Input("theme-store", "data")
)
def update_institution_trends(selected_institutions, metric, theme):
    # Choix du template Plotly en fonction du switch de thème
    template = "mantine_dark" if theme == "dark" else "mantine_light"
    
    # Valeurs par défaut
    if metric is None:
        metric = "enrolment"
    # Si aucune institution n'est sélectionnée, on peut choisir d'afficher toutes.
    if selected_institutions is None or len(selected_institutions) == 0:
        selected_institutions = None
    
    fig = create_institution_trends_figure(metric=metric, institutions=selected_institutions, template=template)
    return fig


@callback(
    Output("corr-institution-chart", "figure"),
    Input("institution-multiselect", "value"),
    Input("institution-metric-dropdown", "value"),
    Input("theme-store", "data")
)
def update_corr_institution_chart(selected_institutions, metric, theme):
    # Choix du template Plotly en fonction du switch de thème
    template = "mantine_dark" if theme == "dark" else "mantine_light"
    
    # Valeurs par défaut
    if metric is None:
        metric = "enrolment"
    # Si aucune institution n'est sélectionnée, on peut choisir d'afficher toutes.
    
    fig = create_corr_institution_figure(mode=metric, institutions=selected_institutions, template=template)
    return fig