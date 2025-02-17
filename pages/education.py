import dash
import dash_mantine_components as dmc
import json
from dash import dcc, html, callback, Output, Input, State, ctx
from dash_extensions import Lottie
import plotly.express as px
from dash_iconify import DashIconify

from figures.education import create_bar_chart_figure, create_line_chart_figure, create_admission_trends_figure, create_institution_trends_figure, create_corr_institution_figure
from utils.config import INSTITUTIONS

dash.register_page(__name__, path="/education")

with open("assets/enrolment.txt", "r") as f:
    enrolment_results = f.read()

with open("assets/intake.txt", "r") as f:
    intake_results = f.read()


layout = dmc.Container(
    fluid=True,
    p="xl",
    children=[
        # ---------- Stores pour suivre l'état interactif ----------
        dcc.Store(id="current-level", data="global"),
        dcc.Store(id="current-parent", data=None),
    
        html.Div(
            style={"width": "100%", "textAlign": "center", "margin": "1rem auto"},
            className="scroll-section",
            children=[
                dmc.Group(
                    align="center",
                    justify="center",
                    children=[
                        DashIconify(icon="mdi:school", height=40, color="#228be6"),
                        dmc.Title("Universities in Singapore", order=1),
                    ],
                    style={"marginBottom": "1rem"}
                ),
                dmc.Text(
                    "Discover the dynamic and competitive landscape of higher education in Singapore.",
                    size="md",
                    style={"marginTop": "0.5rem"}
                ),
                dmc.Space(h="md"),
            ]
        ),

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
                # Partie gauche : Texte explicatif et citation
                html.Div(
                    style={"flex": "1", "maxWidth": "70%", "paddingRight": "1rem"},
                    children=[
                        dmc.Blockquote(
                            "The wealth of a nation lies in its people – their commitment to country and community, their willingness to strive and persevere, their ability to think, achieve and excel. How we raise our young at home and teach them in school will shape our society in the next generation.",
                            cite="- Ministry of Education, Singapore",
                            icon=DashIconify(icon="mdi:format-quote-open", height=20, color="#228be6"),
                            color="primary",
                            radius="lg",
                            style={"textAlign": "left", "width": "100%"}
                        ),
                        dmc.Space(h="md"),
                        dmc.Text(
                            "Singapore’s universities consistently rank among the best in the world, attracting top students from across the globe. "
                            "This page provides an in-depth look at admissions trends, course offerings, and institutional excellence, shedding light on the factors "
                            "that make Singapore a hub for higher education.",
                            size="lg",
                            style={"lineHeight": "1.6", "textAlign": "justify"}
                        ),
                        dmc.Space(h="sm"),
                        dmc.Text(
                            "Explore our interactive data to understand how institutions maintain high standards and to gain insights into the evolving landscape of "
                            "higher education in Singapore.",
                            size="md",
                            style={"lineHeight": "1.6", "textAlign": "justify"}
                        ),
                    ]
                ),
                # Partie droite : Animation Lottie
                html.Div(
                    style={"flex": "1", "maxWidth": "30%", "display": "flex", "justifyContent": "center", "alignItems": "center"},
                    children=[
                        Lottie(
                            options=dict(
                                loop=True,
                                autoplay=True,
                                rendererSettings=dict(preserveAspectRatio="xMidYMid slice")
                            ),
                            width="100%",
                            url="https://lottie.host/55f711be-705a-45f2-8f35-08456dcf6db0/8J4gG2IGrO.json"  # Remplacez par l'URL de votre animation
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
                                         html.Div([
    
                                            # 📌 Titre de la section
                                            dmc.Group(
                                                align="center",
                                                justify="center",
                                                children=[
                                                    DashIconify(icon="mdi:chart-line", height=35, color="#228be6"),
                                                    dmc.Title("Prediction Methodology", order=2),
                                                ],
                                                style={"marginBottom": "1rem", "textAlign": "center"}
                                            ),
                                            
                                            # 📌 Explication en deux colonnes
                                            html.Div(
                                                style={"display": "flex", "gap": "2rem", "justifyContent": "center"},
                                                children=[
                                                    dcc.Markdown(
                                                        """
                                                        ### 🛠 How were the predictions made?

                                                        - **Box-Cox Transformation:**  
                                                        Applied to stabilize variance and normalize data.

                                                        - **Quantile Regression:**  
                                                        Used to predict the median (`q=0.5`), making it robust to outliers.

                                                        - **Inverse Transformation:**  
                                                        After prediction, values were reverted to the original scale.
                                                        """,
                                                        style={"lineHeight": "1.6", "textAlign": "justify", "width": "45%"}
                                                    ),
                                                    dcc.Markdown(
                                                        """
                                                        ### 🔍 Why this approach?

                                                        - **Handles non-linearity:**  
                                                        Box-Cox makes the relationship more linear.

                                                        - **Robust predictions:**  
                                                        Quantile Regression captures trends even with variability.

                                                        - **Better for planning:**  
                                                        Predicting quantiles helps policymakers analyze risks.
                                                        """,
                                                        style={"lineHeight": "1.6", "textAlign": "justify", "width": "45%"}
                                                    ),
                                                ],
                                            ),

                                            dmc.Space(h="xl"),

                                            # 📌 Résultats des modèles avec interprétation
                                            dmc.Group(
                                                align="center",
                                                justify="center",
                                                children=[
                                                    DashIconify(icon="mdi:table", height=30, color="#228be6"),
                                                    dmc.Title("Model Outputs & Interpretation", order=2),
                                                ],
                                                style={"marginBottom": "1rem", "textAlign": "center"}
                                            ),

                                            html.Div(
                                                style={"display": "flex", "gap": "1rem", "justifyContent": "center"},
                                                children=[
                                                    dmc.Card(
                                                        shadow="sm",
                                                        withBorder=True,
                                                        radius="md",
                                                        style={"width": "48%", "padding": "1rem"},
                                                        children=[
                                                            dmc.Group(
                                                                children=[
                                                                    DashIconify(icon="mdi:school", height=25, color="#ff5722"),
                                                                    dmc.Title("Enrolment Model", order=4),
                                                                ]
                                                            ),
                                                            dmc.Space(h="sm"),
                                                            dcc.Markdown(f"```py \n{enrolment_results}\n```"),
                                                            dcc.Markdown( # The value is under box cox transformation so it is not the real value
                                                                """
                                                                **📌 Interpretation:**  
                                                                - **High R² (0.9399):** Model explains most of the variation.  
                                                                - **Intercept:** Large negative value, but **year has a strong positive coefficient (34.2)**.  
                                                                - **Conclusion:** Enrolment is increasing steadily over time.
                                                                """,
                                                                style={"lineHeight": "1.6", "textAlign": "justify"}
                                                            ),
                                                        ]
                                                    ),
                                                    dmc.Card(
                                                        shadow="sm",
                                                        withBorder=True,
                                                        radius="md",
                                                        style={"width": "48%", "padding": "1rem"},
                                                        children=[
                                                            dmc.Group(
                                                                children=[
                                                                    DashIconify(icon="mdi:account-group", height=25, color="#228be6"),
                                                                    dmc.Title("Intake Model", order=4),
                                                                ]
                                                            ),
                                                            dmc.Space(h="sm"),
                                                            dcc.Markdown(f"```py \n{intake_results}\n```"),
                                                            dcc.Markdown(
                                                                # box cox transformation is applied to the value so it is not the real value
                                                                """
                                                                **📌 Interpretation:**  
                                                                - **Lower R² (0.7617):** Model captures trends but leaves some unexplained variability.  
                                                                - **Year Coefficient (163.2):** Strong positive effect on intake.
                                                                - **Conclusion:** Intake is growing rapidly, but with more variability.
                                                                """,
                                                                style={"lineHeight": "1.6", "textAlign": "justify"}
                                                            ),
                                                        ]
                                                    ),
                                                ],
                                            ),

                                            dmc.Space(h="xl"),
                                        ])
                                    ]
                                ),
                            ],
                            value="info",
                            style={"marginBottom": "1rem", "width": "100%", "textAlign": "justify", "margin": "auto"},
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
                            data=INSTITUTIONS,
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
                                "but this rate declines rapidly and stabilizes over time. These trends highlight the competitive landscape of higher education."
                                "On the right, you can explore the correlation between institutions and their respective metrics. This chart allows you to identify which institutions are most closely related in terms of enrolment, intake, and intake rate.",
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