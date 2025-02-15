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
            style={"width": "100%", "textAlign": "center", "marginBottom": "1.5rem", "marginTop": "1rem", "margin": "auto"},
            className="scroll-section",
            children=[
                dmc.Group(
                    children=[
                        DashIconify(icon="mdi:finance", height=40, color="#228be6"), 
                        dmc.Title("Economic Insights", order=1),
                    ],
                    align="center",
                    justify="center",
                    style={"margin": "auto", "textAlign": "center"}
                ),
                dmc.Text(
                    "Explore key economic indicators shaping Singapore’s financial landscape.",
                    size="md",
                    style={"marginTop": "0.5rem"},
                ),
                dmc.Space(h="xl"),
            ],
        ),

        
        # ---------- En-tête ----------
        html.Div(
            style={
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "space-between",
                "gap": "1rem",
                "marginBottom": "2rem",
            },
            className="scroll-section",
            children=[
                # Section gauche : Texte et citation
                html.Div(
                    style={"flex": 1, "maxWidth": "75%"},
                    children=[
                        # Citation inspirante
                        dmc.Blockquote(
                            "Understanding economic trends is key to making informed decisions in business, policy, and everyday life.",
                            cite="- Singapore Economic Review",
                            icon=DashIconify(icon="mdi:lightbulb-on-outline", height=20),
                            color="primary",
                            radius="lg",
                            style={"textAlign": "center", "width": "100%"},
                        ),
                        dmc.Space(h="md"),
                        # Texte introductif
                        dmc.Text(
                            "This dashboard provides an in-depth look at key economic indicators in Singapore, including unemployment rates, wage evolution, "
                            "and cost of living trends. By analyzing these data points, we can better understand the dynamics of the labor market, the impact "
                            "of inflation, and how salaries have evolved over time.",
                            size="lg",
                            style={"lineHeight": "1.6", "textAlign": "justify"},
                        ),
                        dmc.Space(h="sm"),
                        dmc.Text(
                            "With interactive charts and visualizations, you can explore various aspects of Singapore’s economy and gain insights into "
                            "how these factors influence everyday life. Whether you're a researcher, policymaker, or simply curious about economic trends, "
                            "this page offers valuable data-driven perspectives.",
                            size="md",
                            style={"lineHeight": "1.6", "textAlign": "justify"},
                        ),
                    ],
                ),

                # Section droite : Animation Lottie
                html.Div(
                    style={"flex": 1, "maxWidth": "25%", "display": "flex", "justifyContent": "center"},
                    children=[
                        Lottie(
                            options=dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio="xMidYMid slice")),
                            width="100%",
                            url="https://lottie.host/a3d30bc7-499f-4425-af0c-86d35bdce3ff/YovYlOMFwS.json"
                        )
                    ]
                ),
            ],
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
                    "The chart above shows the unemployment rate of Singapore and in major cities in the world. "
                    "We can see that the unemployment rate in Singapore is lower than in other major cities. "
                    "This indicates a strong labor market and a relatively low level of unemployment in the country. "
                    "The next section will provide more detailed insights into the unemployment trends in Singapore.",
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
                        dmc.Space(h="xl"),
                        html.Div(
                            dmc.Text(
                                "This line chart displays the evolution of the Consumer Price Index (CPI) and the Median Salary Index in Singapore over the years. "
                                "The reference year for both indices is 2019, with values indexed to 100. "
                                "The CPI measures the average change in prices paid by consumers for goods and services, providing insights into inflation rates and "
                                "cost-of-living adjustments. In contrast, the Median Salary Index reflects the median income level of workers, offering a gauge of "
                                "economic prosperity and wage growth. By examining these two indices together, you can gain a holistic view of economic trends and "
                                "understand how price fluctuations impact salary dynamics.",
                                size="md",
                            ),
                            # on aligne le div au milieur de la page
                            style={"margin": "auto", "textAlign": "justify", "display": "inline-block"}
                        ),
                        dmc.Space(h="xl"),
                        html.Div(
                            children=[
                                dmc.MultiSelect(
                                    id="cpi-multiselect",
                                    value=get_cpi_multiselect()[1],
                                    data=get_cpi_multiselect()[0],
                                    placeholder="Select CPI categories",
                                    searchable=True,
                                    style={"width": "75%", "margin": "auto"}
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
                                    className="scroll-section",
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
                                                    "This graph visualizes the partial correlations between economic indicators, controlling for all other variables. "
                                                    "Edges represent statistically significant relationships based on a p-value test, and you can adjust the significance level (alpha) "
                                                    "to filter weaker connections. A lower alpha value results in a sparser graph, showing only the strongest correlations.",
                                                    size="md",
                                                    style={"lineHeight": "1.6", "textAlign": "justify"},
                                                ),
                                                dmc.Space(h="sm"),
                                                dmc.Text(
                                                    "You can interact with the graph by clicking on a node: all connected nodes will be highlighted according to their partial correlation "
                                                    "with the selected node. Positive correlations are shown in red, while negative correlations appear in blue. "
                                                    "A color scale bar below the graph provides a reference for interpreting these relationships.",
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
                            style={"width": "100%", "margin": "auto"}
                        )
                    ],
                    style={"margin": "auto"}
                ),
                dmc.Space(h="xl"),
                dmc.Space(h="xl"),

                # References
                html.Div(
                    children=[
                        dmc.Title("References", order=3, style={"textAlign": "center", "marginBottom": "1rem"}),
                        
                        dmc.Text(
                            "Ministry of Manpower. (2016). Overall Unemployment Rate, Annual (2024) [Dataset]. data.gov.sg. Retrieved February 15, 2025 from ",
                            size="xs",
                            style={"textAlign": "center"}
                        ),
                        dmc.Anchor(
                            "https://data.gov.sg/datasets/d_e3598914c86699a9a36e68190f78c59a/view",
                            href="https://data.gov.sg/datasets/d_e3598914c86699a9a36e68190f78c59a/view",
                            target="_blank",
                            size="xs",
                            style={"textAlign": "center"}
                        ),
                        dmc.Space(h="sm"),
                        
                        dmc.Text(
                            "Ministry of Manpower Singapore. (n.d.). Annual average resident unemployment rate by sex, age and highest qualification attained. Singapore Government. Retrieved February 13, 2025, from 3 ",
                            size="xs",
                            style={"textAlign": "center"}
                        ),
                        dmc.Anchor(
                            "https://stats.mom.gov.sg/Pages/UnemploymentTimeSeries.aspx",
                            href="https://stats.mom.gov.sg/Pages/UnemploymentTimeSeries.aspx",
                            target="_blank",
                            size="xs",
                            style={"textAlign": "center"}
                        ),
                        dmc.Space(h="sm"),
                        
                        dmc.Text(
                            "Singapore Department of Statistics. (2024). Resident Working Persons Aged 15 Years and Over by Planning Area and Industry (General Household Survey 2015) (2025) [Dataset]. data.gov.sg. Retrieved February 15, 2025 from ",
                            size="xs",
                            style={"textAlign": "center"}
                        ),
                        dmc.Anchor(
                            "https://data.gov.sg/datasets/d_962495f413f039655f14cb8a59f44317/view",
                            href="https://data.gov.sg/datasets/d_962495f413f039655f14cb8a59f44317/view",
                            target="_blank",
                            size="xs",
                            style={"textAlign": "center"}
                        ),
                        dmc.Space(h="sm"),
                        
                        dmc.Text(
                            "Singapore Department of Statistics. (2024). Resident Working Persons Aged 15 Years and Over by Planning Area and Gross Monthly Income from Work (General Household Survey 2015) (2025) [Dataset]. data.gov.sg. Retrieved February 15, 2025 from ",
                            size="xs",
                            style={"textAlign": "center"}
                        ),
                        dmc.Anchor(
                            "https://data.gov.sg/datasets/d_bb771c5189ce18007621533dd36142bb/view",
                            href="https://data.gov.sg/datasets/d_bb771c5189ce18007621533dd36142bb/view",
                            target="_blank",
                            size="xs",
                            style={"textAlign": "center"}
                        ),
                        dmc.Space(h="sm"),
                        
                        dmc.Text(
                            "Urban Redevelopment Authority. (2023). Master Plan 2019 Planning Area Boundary (No Sea) (2024) [Dataset]. data.gov.sg. Retrieved February 15, 2025 from ",
                            size="xs",
                            style={"textAlign": "center"}
                        ),
                        dmc.Anchor(
                            "https://data.gov.sg/datasets/d_4765db0e87b9c86336792efe8a1f7a66/view",
                            href="https://data.gov.sg/datasets/d_4765db0e87b9c86336792efe8a1f7a66/view",
                            target="_blank",
                            size="xs",
                            style={"textAlign": "center"}
                        ),
                        dmc.Space(h="sm"),
                        
                        dmc.Text(
                            "Singapore Department of Statistics. (2023). Consumer Price Index (CPI), 2019 As Base Year, Monthly (2025) [Dataset]. data.gov.sg. Retrieved February 15, 2025 from ",
                            size="xs",
                            style={"textAlign": "center"}
                        ),
                        dmc.Anchor(
                            "https://data.gov.sg/datasets/d_de7e93a1d0e22c790516a632747bf7f0/view",
                            href="https://data.gov.sg/datasets/d_de7e93a1d0e22c790516a632747bf7f0/view",
                            target="_blank",
                            size="xs",
                            style={"textAlign": "center"}
                        )
                    ],
                    style={"marginTop": "2rem", "textAlign": "center"}
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