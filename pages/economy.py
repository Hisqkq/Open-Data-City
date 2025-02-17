import dash
import dash_mantine_components as dmc
from dash import dcc, html, callback, Output, Input, no_update, callback_context
from dash_extensions import Lottie
from dash_iconify import DashIconify

from utils.colors import get_node_color
from components.colorbar import create_colorbar
from services.data.process_economic_data import get_cpi_multiselect, compute_partial_correlation_matrix
from figures.economy import create_unemployment_bar_chart, create_overal_unemployment_line, create_unemployment_residents_line_chart, create_cpi_salary_line_chart_mantine, create_cytoscape_graph

dash.register_page(__name__, path="/economy")

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
                            "The economy is the start and end of everything. You can't have successful education reform or any other reform if you don't have a strong economy.",
                            cite="- David Cameron",
                            icon=DashIconify(icon="mdi:lightbulb-on-outline", height=20, color="#228be6"),
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
                    className="scroll-section",
                    children=[
                        # Titre de la section
                        html.Div(
                            dmc.Title("Evolution of Unemployment in Singapore", order=2, style={"textAlign": "center"}),
                            style={"width": "100%"}
                        ),
                        dmc.Space(h="xl"),
                        
                        # Phrase d'introduction
                        dmc.Text(
                            "Before delving into the trends, it is important to define key terms used in this analysis:",
                            size="lg",
                            style={"textAlign": "center", "marginBottom": "1rem"}
                        ),
                        
                        # Trois cartes côte à côte pour les définitions
                        dmc.SimpleGrid(
                            cols=3,
                            spacing="lg",
                            style={"maxWidth": "80%", "margin": "auto"},
                            children=[
                                # Carte pour Unemployment
                                dmc.Card(
                                    withBorder=True,
                                    shadow="sm",
                                    radius="md",
                                    style={"padding": "1rem"},
                                    children=[
                                        dmc.CardSection(
                                            dmc.Group(
                                                children=[
                                                    DashIconify(icon="mdi:account-off", height=30, color="#ff7f0e"),
                                                    dmc.Text("Unemployment", fw=500, size="md")
                                                ]
                                            )
                                        ),
                                        dcc.Markdown(
                                            """
                **Definition:**

                Unemployed persons refer to people who are not working but are actively looking and available for jobs.    
                *(Source: Singapore Department of Statistics)*
                                            """,
                                            style={"textAlign": "justify", "lineHeight": "1.6", "fontSize": "14px"}
                                        )
                                    ]
                                ),
                                # Carte pour Residents
                                dmc.Card(
                                    withBorder=True,
                                    shadow="sm",
                                    radius="md",
                                    style={"padding": "1rem"},
                                    children=[
                                        dmc.CardSection(
                                            dmc.Group(
                                                children=[
                                                    DashIconify(icon="mdi:account-check", height=30, color="#1f77b4"),
                                                    dmc.Text("Residents", fw=500, size="md")
                                                ]
                                            )
                                        ),
                                        dcc.Markdown(
                                            """
                **Definition:**

                Singapore residents refer to citizens or non-citizens who have been granted permanent residence in Singapore.   
                *(Source: Singapore Department of Statistics)*
                                            """,
                                            style={"textAlign": "justify", "lineHeight": "1.6", "fontSize": "14px"}
                                        )
                                    ]
                                ),
                                # Carte pour Non-residents
                                dmc.Card(
                                    withBorder=True,
                                    shadow="sm",
                                    radius="md",
                                    style={"padding": "1rem"},
                                    children=[
                                        dmc.CardSection(
                                            dmc.Group(
                                                children=[
                                                    DashIconify(icon="mdi:account-search", height=30, color="#2ca02c"),
                                                    dmc.Text("Non-residents", fw=500, size="md")
                                                ]
                                            )
                                        ),
                                        dcc.Markdown(
                                            """
                **Definition:**

                The non-resident population comprised foreigners who were working, studying or living in Singapore but not granted permanent residence, excluding tourists and short-term visitors.   
                *(Source: Singapore Department of Statistics)*
                                            """,
                                            style={"textAlign": "justify", "lineHeight": "1.6", "fontSize": "14px"}
                                        )
                                    ]
                                ),
                            ]
                        ),
                        dmc.Space(h="xl"),
                    ],
                    style={"padding": "1rem"}
                ),

                dmc.Space(h="lg"),
                
                # ---------- Section 1: Overall Unemployment (text + graph side by side) ----------
                html.Div(
                    className="scroll-section",
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
                                        dmc.Title("Overall Unemployment Trend", order=3, style={"margin": "0"})
                                    ],
                                ),
                                dmc.Text(
                                    "The graph on the right shows the overall unemployment rate in Singapore, including both residents and non-residents. "
                                    "This provides a broad perspective of the labor market dynamics over the years. "
                                    "We can see that Singapore's employment situation has always been stable since 1992, the lowest unemployment rate was in 1997 with 1.4% unemployed persons.",
                                    size="md",
                                    style={"lineHeight": "1.6", "textAlign": "justify"}
                                )
                            ],
                            style={"flex": "1"}
                        ),
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
                    className="scroll-section",
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
                html.Div(
                    className="scroll-section",
                    style={
                        "display": "flex",
                        "flexWrap": "wrap",
                        "justifyContent": "center",
                        "alignItems": "stretch",
                        "gap": "1rem",
                        "width": "90%",
                        "margin": "auto"
                    },
                    children=[
                        dmc.Card(
                            withBorder=True,
                            shadow="sm",
                            radius="md",
                            style={"flex": "1", "minWidth": "250px", "padding": "1rem"},
                            children=[
                                dmc.Group(
                                    align="center",
                                    justify="center",
                                    children=[
                                        DashIconify(icon="mdi:gender-male-female", height=30, color="#1f77b4"),
                                        dmc.Title("By Sex", order=4, style={"margin": "0"})
                                    ]
                                ),
                                dmc.Space(h="sm"),
                                dmc.Text(
                                    "Our analysis indicates that male unemployment rates are generally slightly lower than those for females. "
                                    "However, fluctuations occur during economic downturns, highlighting persistent gender disparities.",
                                    size="sm",
                                    style={"textAlign": "justify", "lineHeight": "1.5"}
                                ),
                            ]
                        ),
                        dmc.Card(
                            withBorder=True,
                            shadow="sm",
                            radius="md",
                            style={"flex": "1", "minWidth": "250px", "padding": "1rem"},
                            children=[
                                dmc.Group(
                                    align="center",
                                    justify="center",
                                    children=[
                                        DashIconify(icon="mdi:account-child", height=30, color="#ff7f0e"),
                                        dmc.Title("By Age", order=4, style={"margin": "0"})
                                    ]
                                ),
                                dmc.Space(h="sm"),
                                dmc.Text(
                                    "Analysis by age shows that younger workers (15-24) face higher unemployment rates compared to older groups. "
                                    "The trend suggests that experience plays a key role in employment stability.",
                                    size="sm",
                                    style={"textAlign": "justify", "lineHeight": "1.5"}
                                ),
                            ]
                        ),
                        dmc.Card(
                            withBorder=True,
                            shadow="sm",
                            radius="md",
                            style={"flex": "1", "minWidth": "250px", "padding": "1rem"},
                            children=[
                                dmc.Group(
                                    align="center",
                                    justify="center",
                                    children=[
                                        DashIconify(icon="mdi:book-open-page-variant", height=30, color="#2ca02c"),
                                        dmc.Title("By Qualification", order=4, style={"margin": "0"})
                                    ]
                                ),
                                dmc.Space(h="sm"),
                                dmc.Text(
                                    "Since 2012, individuals with lower qualifications tend to have lower unemployment rates. "
                                    "However",
                                    size="sm",
                                    style={"textAlign": "justify", "lineHeight": "1.5"}
                                ),
                            ]
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
                dmc.Group(
                    children=[
                        # icone de carte
                        DashIconify(icon="material-symbols:map-search-outline-rounded", height=40, color="#228be6"),
                        dmc.Title("Working Residents by Salary and Population", order=2),
                    ],
                ),
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
                    style={"width": "100%", "height": "500px", "border": "none"}),
                dmc.Space(h="md"),
                html.Div(
    children=[
        dmc.Text("Map Observations", size="lg", style={"marginBottom": "0.5rem", "textAlign": "center"}),
        dcc.Markdown(
                        """
            - **Tanglin** stands out with a median salary exceeding **12,000 SGD**—the highest among the areas. Despite this, Tanglin is not among the most populated regions, suggesting that it is home to a relatively small, affluent group.
            - In most areas, the median salary hovers around **3,500 SGD**, particularly in densely populated regions such as **Jurong West, Woodlands,** and **Tampines**, which are marked by a deep red background.
            - Overall, the most populated areas tend to be slightly off-center. Conversely, areas closer to the city center exhibit higher median salaries, indicating that living in central districts requires a better income.
                        """,
                        style={
                            "lineHeight": "1.6",
                            "textAlign": "justify",
                            "fontSize": "16px",
                            "maxWidth": "80%",
                            "margin": "auto"
                        }
                    )
                ],
                style={"width": "100%", "marginTop": "1rem", "marginBottom": "1rem"}
            )

                
            ]
        ),

        dmc.Space(h="xl"),

        # ---------- Section 3: CPI and Median Salary index Line Chart ----------
                
                html.Div(
                    className="scroll-section",
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
                                style={"textAlign": "justify", "width": "80%", "margin": "auto"}
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
                                    children=[
                                        dcc.Markdown(
                                            """
                                **Key Observations:**

                                - The **Communication** field has shown a decreasing trend over the years, whereas most other fields have generally increased since 2001.
                                - The **Median Salary Index** has seen a substantial rise, climbing from an index value of **52** in 2001 to **113** in 2023.
                                - Between **2011** and **2017**, the **Housing & Utilities** category maintained relatively high index values, ranging between **109** and **114** compared to the 2019 baseline.
                                - The category with the most significant increase is **Transport** (including cars, motorcycles, and public transport), which reached an index of **131** in 2023.

                                These observations illustrate the dynamic nature of Singapore's economic landscape. However, it remains challenging to discern the interdependencies between the different CPI categories. This complexity motivates the subsequent network analysis using partial correlations to better understand the relationships between inflation trends across various categories.
                                            """,
                                            style={
                                                "lineHeight": "1.6",
                                                "fontSize": "16px",
                                                "textAlign": "justify",
                                                "maxWidth": "80%",
                                                "margin": "auto",
                                                "padding": "1rem",
                                                "border": "1px solid #ccc",
                                                "borderRadius": "8px",
                                            }
                                        )
                                    ],
                                    style={"marginTop": "0.5rem", "marginBottom": "0.5rem"}
                                ),
                                dmc.Space(h="xl"),

                                ## Network
                                dmc.Group(
                                    align="center",
                                    justify="center",
                                    children=[
                                        DashIconify(icon="mdi:graph-outline", height=35),
                                        dmc.Title("Partial Correlation Graph", order=3),
                                    ],
                                ),
                                dmc.Space(h="xl"),
                                html.Div(
    style={
        "display": "flex",
        "justifyContent": "center",
        "gap": "2rem",
        "maxWidth": "90%",
        "margin": "auto"
    },
    children=[
        # Carte pour le concept mathématique
        dmc.Card(
            withBorder=True,
            shadow="sm",
            radius="md",
            style={"flex": "1", "padding": "1rem"},
            children=[
                dmc.Group(
                    align="center",
                    justify="center",
                    children=[
                        DashIconify(icon="mdi:math-compass", height=30, color="#228be6"),
                        dmc.Title("Mathematical Concept", order=4, style={"margin": "0", "textAlign": "center"})
                    ]
                ),
                dcc.Markdown(
                    """
                    ### Partial Correlation  

                    The **partial correlation** between two variables $X^{(i)}$ and $X^{(j)}$, given a set of variables $X^{(k)}$ (with $k \\neq i, j$), is defined as:

                    $$
                    \\rho_{ij} = -\\frac{K_{ij}}{\\sqrt{K_{ii} K_{jj}}}
                    $$

                    where $K_{ij}$ are the elements of the **precision matrix** (the inverse of the covariance matrix $\Sigma$).  

                    This metric quantifies the direct relationship between $X^{(i)}$ and $X^{(j)}$ after removing the effects of other variables.  
                    It is particularly useful for identifying hidden associations in a multivariate dataset.
                    """,
                    mathjax=True,
                    style={
                        "textAlign": "justify",
                        "lineHeight": "1.6",
                        "fontSize": "16px",
                        "marginTop": "1rem"
                    }
                )

                                ]
                            ),
                            dmc.Card(
                                withBorder=True,
                                shadow="sm",
                                radius="md",
                                style={"flex": "1", "padding": "1rem"},
                                children=[
                                    dmc.Group(
                                        align="center",
                                        justify="center",
                                        children=[
                                            DashIconify(icon="mdi:code-tags", height=30, color="#228be6"),
                                            dmc.Title("Simplified Python Code", order=4, style={"margin": "0", "textAlign": "center"})
                                        ]
                                    ),
                                    dmc.Space(h="sm"),
                                dmc.Code(
                                    """def compute_partial_correlation_matrix(df, alpha=0.05):

            df_std = (df - df.mean()) / df.std()
            precision = np.linalg.inv(df_std.corr().values)
            n = df_std.shape[1]
            corr_partial = np.zeros((n, n))
            p_vals = np.zeros((n, n))

            for i, j in combinations(range(n), 2):
                corr_partial[i, j] = corr_partial[j, i] = -precision[i, j] / np.sqrt(precision[i, i] * precision[j, j])
                z = 0.5 * np.log((1 + corr_partial[i, j]) / (1 - corr_partial[i, j])) * np.sqrt(df_std.shape[0] - n)
                p_vals[i, j] = p_vals[j, i] = 2 * (1 - scipy.stats.norm.cdf(abs(z)))
            adj_matrix = (p_vals < alpha / (n * (n - 1) / 2)).astype(int)

            return adj_matrix, corr_partial, df.columns.tolist()""",
                                    block=True,
                                )
                             ]
                        )

                                ]
                            ),
                            dmc.Space(h="xl"),
                                html.Div(
                                    style={
                                        "display": "flex",
                                        "gap": "2rem",
                                        "alignItems": "center",
                                        "justifyContent": "center",
                                        "width": "90%",
                                        "margin": "auto"
                                    },
                                    className="scroll-section",
                                    children=[
                                        # Section gauche : Texte explicatif
                                        html.Div(
                                            style={"flex": 1, "maxWidth": "30%"},
                                            children=[
                                                dcc.Markdown(
                                                        """
                                            **Graph Explanation:**

                                            This graph visualizes the partial correlations between economic indicators, controlling for all other variables.  
                                            Edges represent statistically significant relationships based on a p-value test. Adjust the significance level (alpha) using the input below to filter weaker connections (lower alpha values yield a sparser graph).  

                                            **Interactivity:**

                                            - Click on a node to highlight all connected nodes according to their partial correlation with the selected node.
                                            - Positive correlations are shown in red, while negative correlations appear in blue.
                                            - A colorbar beside the graph provides a reference for interpreting the correlation values (ranging from -1 to 1).
                                                        """,
                                                        style={
                                                            "margin": "auto",
                                                            "textAlign": "justify",
                                                            "lineHeight": "1.6",
                                                        }
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
                                            style={"flex": 2, "display": "flex", "flexDirection": "column", "alignItems": "center", "border": "1px solid #ccc", "borderRadius": "8px"},
                                            children=[
                                                html.Div(id="cytoscape-graph", children=create_cytoscape_graph(theme="dark"), 
                                                        style={"width": "100%"}),
                                                html.Div(id="colorbar-container", children=create_colorbar(), 
                                                        style={"marginTop": "1rem"}),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                            style={"width": "100%", "margin": "auto"}
                        )
                    ],
                    style={"margin": "auto"}
                ),
                dmc.Space(h="xl"),

                # card pour l'interpretation du graph avec deux blocks de text les uns a coté des autres
                dmc.Card(
                    shadow="sm",
                    withBorder=True,
                    padding="lg",
                    className="scroll-section",
                    children=[
                        dmc.Group(
                            align="center",
                            justify="center",
                            children=[
                                # icone avec une loupe
                                DashIconify(icon="mdi:magnify", height=35, color="#228be6"),
                                dmc.Title("Graph interpretation", order=3, style={"margin": "0", "textAlign": "center"})
                            ]
                        ),
                        dmc.Space(h="md"),
                        dmc.Group(
                            children=[
                                dcc.Markdown(
                                    """
                        **Adjusting the Alpha Value**

                        If you lower the **alpha value**, you will notice that the graph becomes **less dense** with fewer edges connecting the nodes. This reduction indicates that only the most **significant relationships** are retained, minimizing the chance of spurious connections. For example, setting a very low alpha value may reveal that the *Median Salary Index* is predominantly linked to **Alcohol & Tobacco**, **Education**, and **Food**.
                                    """,
                                    style={
                                        "lineHeight": "1.6",
                                        "textAlign": "justify",
                                        "fontSize": "16px",
                                        "maxWidth": "45%",
                                        "margin": "auto"
                                    }
                                ),
                                dcc.Markdown(
                                    """
                        **Interpreting the Graph**

                        The graph also highlights the **nature of the relationships** between variables. For instance, a **negative correlation** between *Education* and *Transport* suggests that as the cost of education increases, transportation costs tend to decrease. Conversely, a **positive correlation** between *Housing & Utilities* and *Healthcare* implies that rising housing and utility prices are accompanied by increased healthcare costs.
                                    """,
                                    style={
                                        "lineHeight": "1.6",
                                        "textAlign": "justify",
                                        "fontSize": "16px",
                                        "maxWidth": "45%",
                                        "margin": "auto"
                                    }
                                ),
                            ],
                            style={"display": "flex", "justifyContent": "space-between", "gap": "2rem"}
                        )

                    ],
                    style={"margin": "auto", "width": "90%"}
                ),
                

                dmc.Space(h="xl"),
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