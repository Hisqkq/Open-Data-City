import dash
import dash_mantine_components as dmc
from dash import html, dcc
from dash_iconify import DashIconify

dash.register_page(__name__, path="/")

layout = dmc.Container(
    fluid=True,
    p="xl",
    className="scroll-section",
    children=[

        # 📌 Titre principal
        dmc.Group(
            align="center",
            justify="center",
            children=[
                dmc.Title("Welcome to Singapore Open Data", order=1),
            ],
            style={"marginBottom": "1rem"}
        ),
        
        dmc.Text(
            [
                "Explore our interactive insights on key themes in Singapore: ",
                dmc.Text("Education", c="blue", span=True),
                ", ",
                dmc.Text("Housing", c="orange", span=True),
                ", and ",
                dmc.Text("Economy", c="green", span=True),
                "."
            ],
            size="lg",
            style={"marginBottom": "2rem", "textAlign": "center"}
        ),


        # 🏗️ Cartes des thèmes
        dmc.SimpleGrid(
            cols=3,
            spacing="lg",
            style={"alignItems": "stretch"},  # 🔥 Assure que toutes les cartes ont la même hauteur
            children=[
                
                # 📚 Education Card
                dmc.Anchor(
                    dmc.Card(
                        className="hover-card",
                        withBorder=True,
                        shadow="md",
                        radius="md",
                        style={"overflow": "hidden", "textAlign": "center", "display": "flex", "flexDirection": "column", "height": "100%"},
                        children=[
                            dmc.CardSection(
                                html.Img(
                                    src="/assets/img/education.jpg",
                                    style={"width": "100%", "height": "180px", "objectFit": "cover"}
                                )
                            ),
                            dmc.Space(h="sm"),
                            dmc.Group(
                                justify="center",
                                align="center",
                                children=[
                                    DashIconify(icon="tabler:book", height=40, color="#228be6"),
                                    dmc.Title("Education", order=3),
                                ]
                            ),
                            dcc.Markdown(
                                """
                                Analyze **trends in university admissions**, student demographics, and **salary projections** after graduation. 
                                Discover which **universities are the most competitive** and explore **future predictions** on enrolment and intake.
                                """,
                                style={"textAlign": "justify", "padding": "0.5rem", "flex": "1"}
                            ),
                        ]
                    ),
                    href="/education",
                    underline=False
                ),

                # 🏠 Housing Card
                dmc.Anchor(
                    dmc.Card(
                        className="hover-card",
                        withBorder=True,
                        shadow="md",
                        radius="md",
                        style={"overflow": "hidden", "textAlign": "center", "display": "flex", "flexDirection": "column", "height": "100%"},
                        children=[
                            dmc.CardSection(
                                html.Img(
                                    src="/assets/img/housing.jpg",
                                    style={"width": "100%", "height": "180px", "objectFit": "cover"}
                                )
                            ),
                            dmc.Space(h="sm"),
                            dmc.Group(
                                justify="center",
                                align="center",
                                children=[
                                    DashIconify(icon="tabler:home", height=40, color="#ff7f0e"),
                                    dmc.Title("Housing", order=3),
                                ]
                            ),
                            dcc.Markdown(
                                """
                                Investigate **the rising cost of real estate** and compare **housing prices by town**. 
                                We also provide a **prediction model** to estimate property prices **based on key features**.
                                """,
                                style={"textAlign": "justify", "padding": "0.5rem", "flex": "1"}
                            ),
                        ]
                    ),
                    href="/housing",
                    underline=False
                ),

                # 📊 Economy Card
                dmc.Anchor(
                    dmc.Card(
                        className="hover-card",
                        withBorder=True,
                        shadow="md",
                        radius="md",
                        style={"overflow": "hidden", "textAlign": "center", "display": "flex", "flexDirection": "column", "height": "100%"},
                        children=[
                            dmc.CardSection(
                                html.Img(
                                    src="/assets/img/economy.jpg",
                                    style={"width": "100%", "height": "180px", "objectFit": "cover"}
                                )
                            ),
                            dmc.Space(h="sm"),
                            dmc.Group(
                                justify="center",
                                align="center",
                                children=[
                                    DashIconify(icon="tabler:chart-bar", height=40, color="#2ca02c"),
                                    dmc.Title("Economy", order=3),
                                ]
                            ),
                           dcc.Markdown(
                                """
                                Track **employment & unemployment trends**, **salary growth**, and **inflation rates**.  
                                Our analysis explores **partial correlations** between economic indicators and their **long-term evolution**.
                                """,
                                style={"textAlign": "justify", "padding": "0.5rem", "flex": "1"}
                            ),
                        ]
                    ),
                    href="/economy",
                    underline=False
                ),

            ]
        ),

        dmc.Space(h="xl"),
    ],
    style={"padding": "1rem"}
)
