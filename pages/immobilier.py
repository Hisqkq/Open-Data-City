import dash
import dash_mantine_components as dmc
from dash import dcc, html
from dash_extensions import Lottie
import plotly.express as px
import dash_leaflet as dl
from dash import Output, Input, dcc, State
from dash_iconify import DashIconify
import pandas as pd
from figures.immobilier_fig import create_line_chart_figure_introduction, create_table_figure_introduction, create_line_chart_figure_history_price, create_bar_chart_figure
from services.maps.map_immo import create_map
from services.data.process_data_immo import process_town_street
from models.pred_immobilier import predict_immobilier

from utils.config import TOWNS, CODE_OPTUNA, CODE_TRAIN_TEST_SPLIT

dash.register_page(__name__, path="/housing")

layout = dmc.Container(
    fluid=True,
    p="xl",
    children=[

         # Page Title
        html.Div(
            style={
                "width": "100%",
                "textAlign": "center",
                "margin": "auto",
                "marginTop": "1rem",
            },
            className="scroll-section",
            children=[
                dmc.Group(
                    children=[
                        DashIconify(icon="mdi:home", height=40, color="#228be6"),
                        dmc.Title("Real Estate Insights", order=1),
                    ],
                    align="center",
                    justify="center",
                    style={"margin": "auto", "textAlign": "center"}
                ),
                dmc.Text(
                    "Discover key trends and dynamics shaping Singapore's property market.",
                    size="md",
                    style={"marginTop": "0.5rem"}
                ),
                dmc.Space(h="xl"),
            ],
        ),

        # Main Section: Text & Animation side-by-side
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
                # Left Column: Explanatory text and blockquote
                html.Div(
                    style={"flex": 1, "maxWidth": "65%"},
                    children=[
                        dmc.Blockquote(
                            "Real estate cannot be lost or stolen, nor can it be carried away. Purchased with common sense, paid for in full, and managed with reasonable care, it is about the safest investment in the world.",
                            cite="- Franklin D. Roosevelt",
                            icon=DashIconify(icon="mdi:lightbulb-on-outline", height=20, color="#228be6"),
                            color="primary",
                            radius="lg",
                            style={"textAlign": "center", "width": "100%"}
                        ),
                        dmc.Space(h="md"),
                        dmc.Text(
                            "Singapore's property market has experienced remarkable growth in recent years. This dashboard explores key metrics including "
                            "price per square meter, regional disparities, and market trends. Notably, central areas with high property values often have a "
                            "lower population density, while suburban regions reveal different dynamics. Understanding these nuances is essential for gauging "
                            "housing affordability and planning future developments.",
                            size="lg",
                            style={"lineHeight": "1.6", "textAlign": "justify"}
                        ),
                        dmc.Space(h="sm"),
                        dmc.Text(
                            "Through these insights, we aim to provide a comprehensive view of Singapore's real estate landscape, enabling informed decisions "
                            "for investors, policymakers, and residents.",
                            size="md",
                            style={"lineHeight": "1.6", "textAlign": "justify"}
                        ),
                    ]
                ),
                # Right Column: Animation
                html.Div(
                    style={"flex": 1, "maxWidth": "35%", "display": "flex", "justifyContent": "center"},
                    children=[
                        Lottie(
                            options=dict(
                                loop=True,
                                autoplay=True,
                                rendererSettings=dict(preserveAspectRatio="xMidYMid slice")
                            ),
                            width="100%",
                            url="assets/img/Animation - 1738836928686.json"
                        )
                    ]
                ),
            ],
        ),
        dmc.Space(h="xl"),

        # ---------- Section 1: Overall trend price (text + graph side by side) ----------
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
                                dmc.Title("Price per Square Metre Over the Last 8 Years", order=3, style={"margin": "0"})
                                ],
                        ),
                        dmc.Space(h="xl"),
                        dmc.Text(
                            "A spectacular surge in property prices! Since mid-2020, prices per square meter have experienced a meteoric rise, accelerating at an unprecedented pace."
                            "While they seemed relatively stable before this period, the trend reversed, leading to an almost continuous increase."
                            "How far will this price hike go? Will we see a slowdown or correction in the years to come? ",
                            size="md",
                            style={"lineHeight": "1.6", "textAlign": "justify"}
                        )
                    ],
                    style={"flex": "2"}
                ),
                html.Div(
                    children=[
                        create_line_chart_figure_introduction()
                    ],
                    style={"flex": "3"},

                
                )

            ]
        ),
        dmc.Space(h="xl"),

        # ---------- Section 2 :  ----------
        html.Div(
            className="scroll-section",
            children=[
                dmc.Title("Number of homes costing more than a million dollars at resale", order=2),
                dmc.Space(h="md"),

                # --- Première ligne : Table + Mini Card ---
                html.Div(
                    style={"display": "flex", "gap": "2rem", "justifyContent": "center", "alignItems": "stretch"},
                    children=[
                        # Table avec taille réduite et scroll si nécessaire
                        dmc.Card(
                            shadow="sm",
                            withBorder=True,
                            radius="md",
                            style={"flex": 1.5, "padding": "1rem", "maxWidth": "60%"},
                            children=[
                                dmc.Group(
                                    children=[
                                        DashIconify(icon="mdi:table-large", height=25, color="#228be6"),
                                        dmc.Title("Sales Overview", order=4),
                                    ]
                                ),
                                dmc.Space(h="sm"),
                                html.Div(
                                    create_table_figure_introduction(),
                                    style={"overflowX": "auto", "maxWidth": "100%"}  # Permet le scroll horizontal si besoin
                                )
                            ]
                        ),

                        # Mini Card avec du contenu supplémentaire pour équilibrer la hauteur
                        dmc.Card(
                            shadow="sm",
                            withBorder=True,
                            radius="md",
                            style={"flex": 1, "padding": "1rem"},
                            children=[
                                dmc.Group(
                                    children=[
                                        DashIconify(icon="mdi:trending-up", height=25, color="#ff5722"),
                                        dmc.Title("Explosive Growth", order=4),
                                    ]
                                ),
                                dmc.Space(h="sm"),
                                dcc.Markdown(
                                    """
                                    The number of **million-dollar resales** has **tripled** since 2021, reaching **940 sales in 2024**!  
                                    This surge reflects the **rapidly rising prices** in the real estate market. 


                                    This trend has several implications:
                                    - This could have implications for **housing affordability** and **social inequality**.
                                    - It could also indicate a **shift in consumer preferences** towards **luxury properties**.
                                    - Finally, it could be a sign of **speculative behavior** in the market.

                                    """,
                                    style={"lineHeight": "1.6", "textAlign": "justify", "fontSize": "16px"}
                                ),
                            ]
                        ),
                    ]
                ),

                dmc.Space(h="xl"),


                # --- Deuxième ligne : Deux Cards d'Analyse ---
                html.Div(
                    style={"display": "flex", "gap": "2rem", "justifyContent": "center", "alignItems": "start"},
                    children=[
                        # Card 1 - Evolution Analysis
                        dmc.Card(
                            shadow="sm",
                            withBorder=True,
                            radius="md",
                            style={"flex": 1, "padding": "1rem"},
                            children=[
                                dmc.Group(
                                    children=[
                                        DashIconify(icon="mdi:chart-line", height=25, color="#4caf50"),
                                        dmc.Title("Market Evolution", order=4),
                                    ]
                                ),
                                dmc.Space(h="sm"),
                                dcc.Markdown(
                                    """
                                    - **Before 2020**: Less than 100 properties exceeded S$1M.
                                    - **2021**: Sales tripled to **233 transactions**.
                                    - **2023**: The number doubled again to **426**.
                                    - **2024**: A record-breaking **940 sales**!
                                    """,
                                    style={"lineHeight": "1.6", "textAlign": "justify", "fontSize": "16px"}
                                ),
                            ]
                        ),

                        # Card 2 - Future Projections
                        dmc.Card(
                            shadow="sm",
                            withBorder=True,
                            radius="md",
                            style={"flex": 1, "padding": "1rem"},
                            children=[
                                dmc.Group(
                                    children=[
                                        DashIconify(icon="mdi:lightbulb-on-outline", height=25, color="#ff9800"),
                                        dmc.Title("What's Next?", order=4),
                                    ]
                                ),
                                dmc.Space(h="sm"),
                                dcc.Markdown(
                                    """
                                    - Already **120 sales** recorded in early 2025.
                                    - If this trend continues, **a new record is expected**.
                                    - Foreign investments and **rising demand** are fueling the growth.
                                    - Can this rapid rise **sustain itself** in the long run?
                                    """,
                                    style={"lineHeight": "1.6", "textAlign": "justify", "fontSize": "16px"}
                                ),
                            ]
                        ),
                    ]
                ),
            ],
            style={"margin": "auto", "padding": "1.5rem"}
        ),
        dmc.Space(h="xl"),



        # ----------------------
        # Section : Carte avec le switch
        # ----------------------

        dmc.Card(
            shadow="sm",
            withBorder=True,
            padding="lg",
            className="scroll-section",
            children=[
                dmc.Title("Working Residents by Salary and Price per square meter", order=2),
                dmc.Space(h="md"),
                dmc.Text(
                    "This interactive map visualizes the distribution of salaries with either the resale price or the price per square meter."
                    "The map provides a comprehensive overview of the real estate market landscape, highlighting areas with the highest prices and corresponding salary levels.",
                    size="md",
                    style={
                        "lineHeight": "1.6",
                        "textAlign": "justify"
                    }
                ),
                dmc.Text("Select the map to display the distribution of salaries with either the resale price or the price per square meter."),
                dmc.Space(h="md"),
                dmc.SegmentedControl(
                            id="resale_or_pricem2",
                            value="ng",
                            data=[
                                {"value": "Resale", "label": "Resale"},
                                {"value": "Price", "label": "Price per m²"},
                            ],
                            mb=10,
                        ),
                dmc.Space(h="md"),
                dcc.Store(id="selected_map", data="services/maps/folium_map_resale.html"),  # Stocke l'URL du fichier
                dcc.Loading(  # Effet de chargement pendant le changement de carte
                    type="circle",
                    children=html.Iframe(
                        id="map_iframe",
                        srcDoc=open("services/maps/folium_map_resale.html", "r").read(),
                        style={"width": "100%", "height": "500px", "border": "none"}
                    )
                ),
                dmc.Space(h="md"),
                dmc.Paper(
                    style={
                        "display": "flex",
                        "justifyContent": "space-between",
                        "alignItems": "flex-start",
                        "gap": "2rem",
                        "width": "100%",
                        "marginTop": "20px",
                        "padding": "20px",
                        "border": "1px solid #ddd",
                        "borderRadius": "10px",
                     },
                    children=[
                        # Premier texte (gauche)
                        html.Div(
                            style={
                                "flex": "1",
                                "borderRight": "2px solid #ccc",
                                "paddingRight": "1rem",
                            },
                            children=[
                                dmc.Title(
                                    "🔍 Resale Observation",
                                    order=4,
                                    style={"marginBottom": "1rem"},
                                    fw="bold",
                                ),
                                dmc.Text(
                                    "Bukit Timah stands out from other neighborhoods with its highest median salary (SGD 9,000 to SGD 12,000) as well as its highest resale prices.\n"
                                    "Bukit Timah, Queenstown and Bukit Merah are the three areas with the highest resale prices in the city at around SGD 900,000.\n"
                                    "We notice that in the outskirts, Jurong West, Woodlands or Pasir Ris, prices are much lower, around 400,000 SGD.",
                                    size="lg",
                                    style={"textAlign": "left", "lineHeight": "1.6"},
                                ),
                            ],
                        ),
                        # Deuxième texte (droite)
                        html.Div(
                            style={
                                "flex": "1",
                                "paddingLeft": "1rem",
                            },
                            children=[
                                dmc.Title(
                                    "🔍 Price per Square Meter Observation",
                                    order=4,
                                    style={"marginBottom": "1rem"},
                                    fw="bold",
                                ),
                                dmc.Text(
                                    "Concerning the prices per square meter, we notice that the city center districts, namely Bukit Timah, Queenstown and Bukit Merah are those with the highest value.\n"
                                    "Also, in the periphery the price decreases sharply. By clicking on the circles, you can have information on the number of people who work.\n"
                                    "We can conclude that the price per square meter and resale prices are correlated. Which seems to be logical.",
                                    size="lg",
                                    style={"textAlign": "left", "lineHeight": "1.6"},
                                ),
                            ],
                        ),
                    ],
                ),
            ]
        ),

        dmc.Space(h="xl"),
        
        # ----------------------
        # Section : Carte interactive pour la prediction
        # ----------------------
        dmc.Card(
            shadow="sm",
            withBorder=True,
            padding="lg",
            className="scroll-section",
            children=[
                dmc.Title("More information about your town and estimated price of your property or 2025", order=2),
                dmc.Space(h="lg"),
                html.Div(
    style={"width": "100%", "padding": "1rem"},
    children=[
        # =====================
        #      PREMIÈRE LIGNE
        # =====================
        html.Div(
            style={
                "display": "flex",
                "flexWrap": "nowrap",      # Permet de passer en "ligne suivante" si l'écran est trop étroit
                "gap": "0.3rem",
                "width": "100%",
                "minHeight": "60vh",     # Hauteur minimale
            },
            children=[
                # -----------------------------
                # Colonne de gauche (20%)
                # -----------------------------
                html.Div(
                    style={
                        "flex": "0 0 20%",     
                        "minWidth": "250px",
                        "boxSizing": "border-box",
                    },
                    children=[
                        dmc.Paper(
                            style={
                                "height": "100%",
                                "padding": "20px",
                                # "boxSizing": "border-box",
                            },
                            children=[
                                html.H3("Estimate your property!", style={"marginTop": 0, "align": "center"}),
                                dmc.Space(h="md"),
                                html.P("Make your choices to get an estimate :"),

                                dmc.Select(
                                    label="Number of rooms",
                                    id="property-type",
                                    data=[
                                        {"label": "1 ROOM", "value": "1 ROOM"},
                                        {"label": "2 ROOM", "value": "2 ROOM"},
                                        {"label": "3 ROOM", "value": "3 ROOM"},
                                        {"label": "4 ROOM", "value": "4 ROOM"},
                                        {"label": "5 ROOM", "value": "5 ROOM"},
                                        {"label": "EXECUTIVE", "value": "EXECUTIVE"},
                                        {"label": "MULTI-GENERATION", "value": "MULTI-GENERATION"},
                                    ],
                                    placeholder="Select a flat_type",
                                    withScrollArea=False,
                                    mt="md",
                                ),
                                dmc.Space(h="md"),

                                html.Label("Area (m²) :"),
                                dmc.Slider(
                                    id="slider-callback",
                                    min=30,
                                    max=400,
                                    value=30,
                                    marks=[
                                        {"value": 30, "label": "30"},
                                        {"value": 100, "label": "100"},
                                        {"value": 200, "label": "200"},
                                        {"value": 300, "label": "300"},
                                        {"value": 400, "label": "400"},
                                    ],
                                    mb=35,
                                ),
                                dmc.Text(id="slider-output"),
                                dmc.Space(h="md"),

                                dmc.Select(
                                    label="Town : ",
                                    id="quartier-select",
                                    data=TOWNS,
                                    placeholder="Select a town",
                                    withScrollArea=True,
                                    mt="md",
                                ),
                                dmc.Space(h="md"),
                                dmc.Select(
                                    label="Street",
                                    id="street-select",
                                    data=[],  # Commence vide, mis à jour via callback
                                    placeholder="Select a street",
                                    withScrollArea=True,
                                    mt="md",
                                ),
                                dmc.Space(h="md"),
                            ],
                        )
                    ],
                ),

                # -----------------------------
                # Colonne centrale (40%) : Carte
                # -----------------------------
                html.Div(
                    style={
                        "flex": "0 0 40%",
                        "minWidth": "300px",
                        "boxSizing": "border-box",
                    },
                    children=[
                        dmc.Paper(
                            style={
                                "height": "100%",
                                "padding": "10px",
                                "boxSizing": "border-box",
                            },
                            children=[
                                create_map(),  # ta carte Leaflet
                            ],
                        )
                    ],
                ),

                # -----------------------------
                # Colonne de droite (40%) : Graphiques
                # -----------------------------
                html.Div(
                    style={
                        "flex": "0 0 39%",
                        "minWidth": "300px",
                        "boxSizing": "border-box",
                    },
                    children=[
                        dmc.Paper(
                            style={
                                "height": "100%",
                                "padding": "20px",
                                # "boxSizing": "border-box",
                            },
                            children=[
                                dmc.SegmentedControl(
                                    id="graph-toggle",
                                    value="line-chart",  # Valeur par défaut
                                    data=[
                                        {"value": "line-chart", "label": "Price evolution"},
                                        {"value": "bar-chart", "label": "Average price"},
                                    ],
                                    fullWidth=True,
                                    style={"marginBottom": "5px"},
                                ),
                                dmc.Paper(
                                    id="line-chart-container",
                                    children=[dcc.Graph(id="price-trend-graph")],
                                    # style={"display": "block"},  # Par défaut visible
                                ),
                                dmc.Paper(
                                    id="bar-chart-container",
                                    children=[dcc.Graph(id="price-bar-chart")],
                                    style={"display": "none"},   # Caché par défaut
                                ),
                                dcc.Store(id="selected-town", data="Ang Mo Kio"),
                                dmc.Paper(id="town-name", children="Town : Ang Mo Kio", style={"textAlign": "center"}),
                            ],
                        ),

                        dmc.Space(h="md"),
                    ],
                ),
            ],
        ),

        # =====================
        #      DEUXIÈME LIGNE
        # =====================
        html.Div(
            style={
                "display": "flex",
                "flexWrap": "wrap",
                "gap": "2rem",
                "width": "100%",
                "marginTop": "20px",
                "padding": "20px",
                "border": "1px solid #ddd",
                "borderRadius": "10px",
            },
            children=[
                # 1) Premier bloc (gauche)
                html.Div(
                    style={
                        "flex": "1",
                        "minWidth": "200px",
                        "boxSizing": "border-box",
                    },
                    children=[
                        dmc.Title(
                            "Information",
                            order=4,
                            style={"marginBottom": "1rem"},
                            fw="bold",
                        ),
                        dmc.Text(
                            "Please fill in the information via the dropdown and the slider to estimate your property!\n",
                            size="lg",
                            style={"textAlign": "left", "lineHeight": "1.6"},
                        ),
                    ],
                ),

                # 2) Deuxième bloc (milieu)
                html.Div(
                    style={
                        "flex": "1",
                        "minWidth": "200px",
                        "boxSizing": "border-box",
                        "textAlign": "center",
                        "borderLeft": "1px solid #ddd",
                        "borderRight": "1px solid #ddd",
                    },
                    children=[
                        dmc.Title(
                            "It's time to estimate your property!",
                            order=4,
                            style={"marginBottom": "1rem"},
                            fw="bold",
                        ),
                        dmc.Group(
                            style={"display": "flex", "justifyContent": "center", "marginTop": "20px"},
                            children=[
                                dmc.Button("Estimate", id="estimate-btn", color="blue", style={"marginTop": "10px"}, size="lg"),
                            ]
                        ),
                        dmc.Paper(style={"marginTop": "20px"}),  # Séparateur ou bloc vide
                        dmc.Text(
                            id="estimation-result",
                            style={"fontSize": "18px", "fontWeight": "bold", "textAlign": "center"},
                        ),
                    ],
                ),

                # 3) Troisième bloc (droite)
                html.Div(
                    style={
                        "flex": "1",
                        "minWidth": "200px",
                        "boxSizing": "border-box",
                    },
                    children=[
                        dmc.Title(
                            "History of the price per square meter and overview of the real estate prices in your neighborhood",
                            order=4,
                            style={"marginBottom": "1rem"},
                            fw="bold",
                        ),
                        dmc.Text(
                            "Plots\n"
                            "If you click on \"Average price\", you will get an overview of the real estate prices in your neighborhood compared to the city.\n",
                            size="lg",
                            style={"textAlign": "left", "lineHeight": "1.6"},
                        ),
                    ],
                ),
            ],
        ),

        dmc.Space(h="lg"),
    ]
),
                dmc.Space(h="lg"),
                html.Div([
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
                                        # ----- Titre principal -----
                                        dmc.Group(
                                            align="center",
                                            justify="center",
                                            children=[
                                                DashIconify(icon="mdi:chart-line", height=35, color="#228be6"),
                                                dmc.Title("Prediction Methodology", order=2),
                                            ],
                                            style={"marginBottom": "1rem", "textAlign": "center"}
                                        ),
                                        # ----- Grille de 4 cartes -----
                                        html.Div(
                                            style={
                                                "display": "flex",
                                                "flexWrap": "wrap",
                                                "gap": "1rem",
                                                "justifyContent": "center"
                                            },
                                            children=[
                                                # Carte 1 : Model & Data Preparation
                                                dmc.Paper(
                                                    shadow="sm",
                                                    withBorder=True,
                                                    radius="md",
                                                    style={"flex": "0 0 45%", "padding": "1rem"},
                                                    children=[
                                                        dmc.Group(
                                                            align="center",
                                                            children=[
                                                                DashIconify(icon="mdi:database", height=25, color="#2c3e50"),
                                                                dmc.Text("Model & Data Preparation"),
                                                            ],
                                                        ),
                                                        dcc.Markdown(
                                                            """
                                                            **Model Used:** CatBoost Regressor  
                                                            
                                                            The dataset was thoroughly cleaned to remove irrelevant features.  
                                                            Date features (such as month and year) were converted into numerical formats  
                                                            and the lease duration was processed to capture the effective property age.  
                                                            In addition, key categorical features like *town*, *flat_type*, *storey_range*,  
                                                            and *flat_model* were carefully selected to improve model performance.
                                                            """,
                                                            style={"lineHeight": "1.6", "fontSize": "0.9rem"}
                                                        ),
                                                    ],
                                                ),
                                                # Carte 2 : Training Process
                                                dmc.Paper(
                                                    shadow="sm",
                                                    withBorder=True,
                                                    radius="md",
                                                    style={"flex": "0 0 45%", "padding": "1rem"},
                                                    children=[
                                                        dmc.Group(
                                                            align="center",
                                                            children=[
                                                                DashIconify(icon="mdi:play-circle", height=25, color="#2c3e50"),
                                                                dmc.Text("Training Process"),
                                                            ],
                                                        ),
                                                        dcc.Markdown(
                                                            """
                                                            **80/20 Train-Test Split:**  
                                                            
                                                            The data was split into training (80%) and validation (20%) sets to ensure robust evaluation.  
                                                            CatBoost's native Pool was used for efficiently handling categorical features during training.  
                                                            The model was trained for 1500 iterations, employing early stopping to prevent overfitting 
                                                            and to optimize the number of boosting rounds.
                                                            """,
                                                            style={"lineHeight": "1.6", "fontSize": "0.9rem"}
                                                        ),
                                                    ],
                                                ),
                                                # Carte 3 : Hyperparameter Optimization
                                                dmc.Paper(
                                                    shadow="sm",
                                                    withBorder=True,
                                                    radius="md",
                                                    style={"flex": "0 0 45%", "padding": "1rem"},
                                                    children=[
                                                        dmc.Group(
                                                            align="center",
                                                            children=[
                                                                DashIconify(icon="tdesign:setting-1", height=25, color="#2c3e50"),
                                                                dmc.Text("Hyperparameter Optimization"),
                                                            ],
                                                        ),
                                                        dcc.Markdown(
                                                            """
                                                            **Optuna:**  
                                                            
                                                            An advanced hyperparameter tuning framework, **Optuna**, was employed to automatically search for the optimal combination of model parameters.  
                                                            During the optimization process, key parameters such as the learning rate, tree depth, number of iterations, and L2 regularization coefficient were systematically varied using functions like `trial.suggest_float` and `trial.suggest_int`.  
                                                            Optuna utilizes efficient algorithms such as the Tree-structured Parzen Estimator (TPE) to navigate the hyperparameter space, quickly converging on values that balance model complexity and predictive performance.  
                                                            This rigorous tuning process not only improved the model’s accuracy but also enhanced its ability to generalize on unseen data by effectively preventing overfitting.
                                                            """,
                                                            style={"lineHeight": "1.6", "fontSize": "0.9rem"}
                                                        ),
                                                    ],
                                                ),
                                                # Carte 4 : Performance Evaluation
                                                dmc.Paper(
                                                    shadow="sm",
                                                    withBorder=True,
                                                    radius="md",
                                                    style={"flex": "0 0 45%", "padding": "1rem"},
                                                    children=[
                                                        dmc.Group(
                                                            align="center",
                                                            children=[
                                                                DashIconify(icon="mdi:check-circle", height=25, color="#2c3e50"),
                                                                dmc.Text("Performance Evaluation"),
                                                            ],
                                                        ),
                                                        dcc.Markdown(
                                                            """
                                                            **Metrics Assessed:**  
                                                            
                                                            Model performance was evaluated using:
                                                            - **Mean Absolute Error (MAE): 18474.76 SGD**
                                                            - **Root Mean Squared Error (RMSE): 25872.16 SGD**
                                                            - **R² Score: 0.9791**
                                                            
                                                            A high R² score indicates that the model explains most of the variance in property prices,  
                                                            while low MAE and RMSE values confirm that the predictions are accurate and reliable.  
                                                            These metrics collectively validate the model's effectiveness.
                                                            """,
                                                            style={"lineHeight": "1.6", "fontSize": "0.9rem"}
                                                        ),

                                                    ],
                                                ),
                                            ]
                                        ),
                                        dmc.Space(h="xl"),
                                        # ----- Bouton centré en bas -----
                                        html.Div(
                                            style={"textAlign": "center"},
                                            children=[
                                                dmc.Button("Show Code Example", id="show-code-btn", color="blue")
                                            ]
                                        ),
                                        dmc.Space(h="xl"),
                                    ]
                                ),
                            ],
                            value="info",
                            style={"marginBottom": "1rem", "width": "100%", "textAlign": "justify", "margin": "auto"},
                        ),
                    ],
                ),

                    # ----- Modal pour afficher les exemples de code -----
                    dmc.Modal(
                        id="code-modal",
                        title="Code Examples",
                        size="lg",
                        centered=True,
                        children=[
                            dmc.Tabs(
                                value="optuna",
                                children=[
                                    dmc.TabsList(
                                        [
                                            dmc.TabsTab(children=dmc.Text("Optuna Code"), value="optuna"),
                                            dmc.TabsTab(children=dmc.Text("Train Test Split Code"), value="train_test"),
                                        ]
                                    ),
                                    dmc.TabsPanel(
                                        dmc.Code(children=CODE_OPTUNA, block=True, style={"whiteSpace": "pre-wrap"}),
                                        value="optuna",
                                    ),
                                    dmc.TabsPanel(
                                        dmc.Code(children=CODE_TRAIN_TEST_SPLIT, block=True, style={"whiteSpace": "pre-wrap"}),
                                        value="train_test",
                                    ),
                                ]
                            )
                        ],
                        opened=False,
                    )
                ])

            ]
        ),
        dmc.Space(h="xl"),
        html.Div(
                    children=[
                        dmc.Title("References", order=3, style={"textAlign": "center", "marginBottom": "1rem"}),

                        dmc.Text(
                            "Housing & Development Board. (2021). Resale flat prices based on registration date from Jan-2017 onwards (2025) [Dataset]. data.gov.sg. Retrieved February 17, 2025",
                            size="xs",
                            style={"textAlign": "center"}
                        ),
                        dmc.Anchor(
                            "https://data.gov.sg/datasets/d_8b84c4ee58e3cfc0ece0d773c8ca6abc/view",
                            href="https://data.gov.sg/datasets/d_8b84c4ee58e3cfc0ece0d773c8ca6abc/view",
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
                        
                    ],
                    style={"marginTop": "2rem", "textAlign": "center"}
                )
        
    ]
)


# ----- Callback pour ouvrir/fermer la modal -----
@dash.callback(
    Output("code-modal", "opened"),
    Input("show-code-btn", "n_clicks"),
    State("code-modal", "opened"),
    prevent_initial_call=True
)
def toggle_modal(n_clicks, opened):
    return not opened

# Callback pour changer la carte affichée
@dash.callback(
    Output("map_iframe", "srcDoc"),
    Input("resale_or_pricem2", "value"),
)
def update_map(selected_value):
    if selected_value == "Resale":
        map_path = "services/maps/folium_map_resale.html"
    else:
        map_path = "services/maps/folium_map_price.html"

    with open(map_path, "r") as f:
        return f.read()
    

@dash.callback(
    [
        Output("price-trend-graph", "figure"),
        Output("price-bar-chart", "figure"),
        Output("town-name", "children"),
        Output("selected-town", "data"),
        Output("line-chart-container", "style"),
        Output("bar-chart-container", "style"),
        Output("quartier-select", "value"),
    ],
    [Input("geojson-layer", "n_clicks"), Input("graph-toggle", "value"), Input("theme-store", "data"), Input("quartier-select", "value"),],
    State("geojson-layer", "clickData")
)
def update_graph(n_clicks, graph_type, theme, selected_town, clickData):
    if clickData and "properties" in clickData:
        town_name = clickData["properties"]["PLN_AREA_N"].title()
    elif selected_town:
        town_name = selected_town
    else:
        town_name = "Ang Mo Kio" 

    template = "mantine_dark" if theme == "dark" else "mantine_light"

    # Générer les figures
    line_chart_fig = create_line_chart_figure_history_price(town_name, template=template)
    bar_chart_fig = create_bar_chart_figure(town_name, template=template)

    # Gérer l'affichage des graphiques
    if graph_type == "line-chart":
        line_chart_style = {"display": "block"}
        bar_chart_style = {"display": "none"}
    else:
        line_chart_style = {"display": "none"}
        bar_chart_style = {"display": "block"}

    return line_chart_fig, bar_chart_fig, f"Town : {town_name}", town_name, line_chart_style, bar_chart_style, town_name



@dash.callback(Output("slider-output", "children"), Input("slider-callback", "value"))
def update_value(value):
    return f"You have selected: {value}"


@dash.callback(
    Output("street-select", "data"), 
    Input("quartier-select", "value"),
)
def update_street_dropdown(selected_town):
    if not selected_town:
        return []
    streets = process_town_street().get(selected_town, [])
    return [{"label": street, "value": street} for street in streets]

@dash.callback(
    Output("estimation-result", "children"),
    Input("estimate-btn", "n_clicks"),
    State("property-type", "value"),
    State("quartier-select", "value"),
    State("street-select", "value"),
    State("slider-callback", "value"),
)
def estimate_price(n_clicks, flat_type, town, street_name, floor_area_sqm):
    if not n_clicks:
        return "Your estimate coming soon! \n"

    # Vérifier si toutes les entrées nécessaires sont remplies
    if not all([flat_type, town, street_name, floor_area_sqm]):
        return "Please select all required fields. \n"

    # Construire la dataframe pour la prédiction
    input_data = pd.DataFrame([{
        "month": 1,  # Janvier par défaut
        "year": 2025,  # Année suivante
        "town": town,
        "flat_type": flat_type,
        "street_name": street_name,
        "storey_range": "04 TO 06",  # Valeur par défaut
        "floor_area_sqm": floor_area_sqm,
        "flat_model": "Apartment",  # Valeur par défaut
        "lease_commence_date": 2000,  # Valeur par défaut
        "remaining_lease_years": 6.5  # Valeur par défaut
    }])

    # Faire la prédiction
    predicted_price = predict_immobilier(input_data)

    # Retourner le résultat formaté
    return f"Estimated Price: {predicted_price[0]:,.2f} SGD \n"