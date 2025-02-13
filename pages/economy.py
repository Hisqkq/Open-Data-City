import dash
import dash_mantine_components as dmc
from dash import dcc, html, callback, Output, Input, no_update, callback_context
from dash_extensions import Lottie
from dash_iconify import DashIconify

from utils.colors import get_node_color
from services.data.process_economic_data import get_cpi_multiselect, compute_partial_correlation_matrix
from figures.economy import create_unemployment_bar_chart, create_overal_unemployment_line, create_unemployment_residents_line_chart, create_cpi_salary_line_chart_mantine, create_cytoscape_graph

dash.register_page(__name__, path="/economy")

def create_colorbar(theme="dark"):
    # Définition des couleurs en fonction du thème
    text_color = "#ffffff" if theme == "dark" else "#000000"
    border_color = "#ffffff" if theme == "dark" else "#000000"

    return html.Div(
        children=[
            html.Div(
                style={
                    "width": "200px",
                    "height": "20px",
                    "background": "linear-gradient(to right, #0000FF, #FFFFFF, #FF0000)",
                    "border": f"1px solid {border_color}",
                }
            ),
            html.Div(
                style={"display": "flex", "justifyContent": "space-between", "width": "200px"},
                children=[
                    html.Span("-1", style={"color": text_color}),
                    html.Span("0", style={"color": text_color}),
                    html.Span("1", style={"color": text_color}),
                ],
            ),
        ],
        style={"display": "flex", "flexDirection": "column", "alignItems": "center"},
    )




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
        ),
        dmc.Card(
            shadow="sm",
            withBorder=True,
            padding="lg",
            className="scroll-section",
            children=[
                dmc.Title("Working Residents by Salary and Population", order=2),
                dmc.Space(h="md"),
                dmc.Text(
                    "This interactive map visualizes the distribution of working residents in Singapore, segmented by median salary and population. "
                    "The map provides a comprehensive overview of the labor market landscape, highlighting areas with high concentrations of workers "
                    "and their corresponding salary levels. By exploring this data, you can gain insights into the economic dynamics of different regions "
                    "and identify potential opportunities for growth and development.",
                    size="md",
                    style={
                        "lineHeight": "1.6",
                        "textAlign": "justify"
                    }
                ),
                dmc.Space(h="md"),
                html.Iframe(srcDoc=open("services/maps/working_residents_salary_pop_map.html", "r").read(),
                    style={"width": "100%", "height": "500px", "border": "none"})
            ]
        ),

        dmc.Space(h="xl"),

        # ---------- Section 3: CPI and Median Salary index Line Chart ----------
                
                html.Div(
                    children=[
                        html.Div(
                            dmc.Title("Consumer Price Index (CPI) and Median Salary Index", order=2, style={"textAlign": "center"}),
                            style={"width": "100%"}
                        ),
                        html.Div(
                            dmc.Text(
                                "This line chart displays the evolution of the Consumer Price Index (CPI) and the Median Salary Index in Singapore over the years. "
                                "The reference year for both indices is 2019, with values indexed to 100. "
                                "The CPI measures the average change in prices paid by consumers for goods and services, providing insights into inflation rates and "
                                "cost-of-living adjustments. In contrast, the Median Salary Index reflects the median income level of workers, offering a gauge of "
                                "economic prosperity and wage growth. By examining these two indices together, you can gain a holistic view of economic trends and "
                                "understand how price fluctuations impact salary dynamics.",
                                size="md",
                                style={
                                    "lineHeight": "1.6",
                                    "textAlign": "justify",
                                    "marginBottom": "1rem",
                                    "marginTop": "1rem",
                                    "width": "80%",
                                }
                            ),
                            # on aligne le div au milieur de la page
                            style={"margin": "auto", "textAlign": "center"}
                        ),
                        html.Div(
                            children=[
                                dmc.MultiSelect(
                                    id="cpi-multiselect",
                                    value=get_cpi_multiselect()[1],
                                    data=get_cpi_multiselect()[0],
                                    placeholder="Select CPI categories",
                                    searchable=True,
                                    style={"width": "45%", "margin": "auto"}
                                ),
                                html.Div(
                                    create_cpi_salary_line_chart_mantine(),
                                    id="cpi-salary-line-chart"
                                ),

                                html.Div(
                                    style={
                                        "display": "flex",
                                        "gap": "2rem",
                                        "alignItems": "center",
                                        "justifyContent": "center",
                                        "width": "100%",
                                    },
                                    children=[
                                        # Section gauche : Texte explicatif
                                        html.Div(
                                            style={"flex": 1, "maxWidth": "30%"},
                                            children=[
                                                dmc.Group(
                                                    children=[
                                                        DashIconify(icon="mdi:graph-outline", height=35),
                                                        dmc.Title("Partial Correlation Graph", order=3, style={"margin": "0"}),
                                                    ],
                                                ),
                                                dmc.Space(h="md"),
                                                dmc.Text(
                                                    "This graph represents the partial correlations between economic indicators "
                                                    "after controlling for all other variables. It is based on a statistical test "
                                                    "using p-values. You can adjust the significance level (alpha) to filter the edges "
                                                    "shown in the graph. Lower alpha values make the graph more sparse.",
                                                    size="md",
                                                    style={"lineHeight": "1.6", "textAlign": "justify"},
                                                ),
                                                dmc.Space(h="md"),
                                                dmc.NumberInput(
                                                    id="alpha-input",
                                                    min=0,
                                                    max=1,
                                                    allowDecimal=True,
                                                    w=200,
                                                    placeholder="Alpha value",
                                                    value=0.05,
                                                    rightSection=DashIconify(icon="mdi:alpha"),
                                                ),
                                            ],
                                        ),

                                        # Section droite : Graph + Colorbar
                                        html.Div(
                                            style={"flex": 2, "display": "flex", "flexDirection": "column", "alignItems": "center"},
                                            children=[
                                                html.Div(id="cytoscape-graph", children=create_cytoscape_graph(theme="dark"), 
                                                        style={"width": "100%"}),
                                                html.Div(id="colorbar-container", children=create_colorbar(), 
                                                        style={"marginTop": "1rem"}),
                                            ],
                                        ),
                                    ],
                                )

                                    
                            ],
                        )
                    ],
                    style={"margin": "auto"}
                ),
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
    return create_unemployment_residents_line_chart(selected_mode)


@callback(
    Output("cpi-salary-line-chart", "children"),
    Input("cpi-multiselect", "value")
)
def update_cpi_line_chart(selected_columns):
    if not selected_columns:
        selected_columns = None
    
    return create_cpi_salary_line_chart_mantine(cpi_columns=selected_columns)


@callback(
    Output("cytoscape-graph", "children"),
    Output("cytoscape", "stylesheet"),
    Input("alpha-input", "value"),
    Input("theme-store", "data"),
    Input("cytoscape", "tapNodeData"),
    prevent_initial_call=True
)
def update_cytoscape(alpha, theme, tapped_node):
    # Convertir alpha en float et le contraindre à [0,1]
    try:
        alpha = float(alpha)
    except (ValueError, TypeError):
        alpha = 0.05
    if not (0 <= alpha <= 1):
        alpha = 0.05

    # Déterminer le thème
    template = "dark" if theme == "dark" else "light"
    base_text_color = "#ffffff" if template == "dark" else "#000000"
    
    # Créer le graphe Cytoscape
    cyto_graph = create_cytoscape_graph(alpha=alpha, theme=template)
    
    # Définition de la stylesheet de base
    base_stylesheet = [
        {
            "selector": "node",
            "style": {
                "label": "data(label)",
                "font-size": "14px",
                "background-color": "#ff7f0e",
                "color": base_text_color,
                "text-halign": "center",
                "text-valign": "center",
                "width": 16,
                "height": 15
            }
        },
        {
            "selector": "edge",
            "style": {
                "width": "mapData(weight, 0, 1, 1, 5)",
                "line-color": "#666666",
                "curve-style": "bezier"
            }
        },
        {
            "selector": "node:selected",
            "style": {
                "background-color": "red",
                "border-width": 2,
                "border-color": "black",
                "color": base_text_color
            }
        },
        {
            "selector": "edge:selected",
            "style": {
                "line-color": "red",
                "width": 4
            }
        }
    ]
    
    # Calculer la nouvelle stylesheet en fonction du nœud cliqué
    if not tapped_node:
        new_stylesheet = base_stylesheet
    else:
        clicked_id = tapped_node["id"]
        # Recalculer la matrice de corrélations partielles avec le seuil alpha
        adj_matrix, corr_partial, var_names = compute_partial_correlation_matrix(alpha)
        try:
            idx = var_names.index(clicked_id)
        except ValueError:
            new_stylesheet = base_stylesheet
        else:
            new_stylesheet = base_stylesheet.copy()
            # Mettre en évidence le nœud cliqué
            new_stylesheet.append({
                "selector": f'node[id = "{clicked_id}"]',
                "style": {
                    "background-color": "red",
                    "border-width": 3,
                    "border-color": "black",
                    "color": base_text_color
                }
            })
            for i, var in enumerate(var_names):
                if var == clicked_id:
                    continue
                corr_val = corr_partial[idx, i]
                color = get_node_color(corr_val)  # Convertit la corrélation en couleur
                new_stylesheet.append({
                    "selector": f'node[id = "{var}"]',
                    "style": {
                        "background-color": color,
                        "color": base_text_color
                    }
                })
    
    if callback_context.triggered and "tapNodeData" in callback_context.triggered[0]['prop_id']:
        return no_update, new_stylesheet
    else:
        return cyto_graph, new_stylesheet
    

@callback(
    Output("colorbar-container", "children"),
    Input("theme-store", "data")
)
def update_colorbar(theme):
    template = "dark" if theme == "dark" else "light"
    return create_colorbar(theme=template)