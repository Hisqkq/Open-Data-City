import dash
import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

dash.register_page(__name__, path="/about-us")

layout = dmc.Container(
    fluid=True,
    p="xl",
    children=[
        # Titre de la page avec icône
        dmc.Group(
            align="center",
            justify="center",
            children=[
                DashIconify(icon="mdi:account-group", height=40, color="#228be6"),
                dmc.Title("About Us", order=1),
            ],
            style={"marginBottom": "1rem"},
        ),

        # Texte d'introduction
        dmc.Text(
            "This project was developed as part of our university curriculum in Open Data. We, Théo Lavandier and Baptiste Gerbouin, are final-year CMI ISI students passionate about data science, machine and deep learning, data engineering, and data visualization.",
            size="lg",
            style={"marginBottom": "2rem", "textAlign": "center"}
        ),

        # Cartes côte à côte dans une grille
        dmc.SimpleGrid(
            cols=2,
            spacing="lg",

            children=[
                # Carte de Théo Lavandier
                dmc.Card(
                    withBorder=True,
                    shadow="sm",
                    radius="md",
                    w=450,
                    children=[
                        dmc.CardSection(
                            dmc.Image(
                                src="assets/img/Theo.png",
                                h=250,
                                alt="Théo Lavandier"
                            )
                        ),
                        # apart
                        dmc.Group(
                            justify="apart",
                            mt="md",
                            mb="xs",
                            children=[
                                dmc.Text("Théo Lavandier", fw=500),
                            ]
                        ),
                        dmc.Text(
                            "Final-year CMI ISI student passionate about machine learning, deep learning, and data engineering.",
                            size="sm",
                            c="dimmed"
                        ),
                        dmc.Space(h="sm"),
                        dmc.Text(
                            "Academic Background:",
                            fw=500,
                            size="sm"
                        ),
                        dmc.List(
                            [
                                dmc.ListItem("Licence & Master in CMI ISI, University of Bordeaux"),
                                dmc.ListItem("3rd year at Radboud University, Netherlands")
                            ],
                            size="xs",
                            c="dimmed"
                        ),
                        dmc.Space(h="sm"),
                         dmc.Text(
                            "Actually doing an internship at:",
                            fw=500,
                            size="sm"
                        ),
                        dmc.Text(
                            "Airbus - Data Quality for embedded IA, Toulouse",
                            size="sm",
                            c="dimmed"
                        ),
                        dmc.Group(
                            mt="md",
                            children=[
                                dmc.Anchor(
                                    DashIconify(icon="mdi:github", height=25),
                                    href="https://github.com/Hisqkq",  
                                    target="_blank"
                                ),
                                dmc.Anchor(
                                    DashIconify(icon="mdi:linkedin", height=25),
                                    href="https://www.linkedin.com/in/theo-lavandier",  
                                    target="_blank"
                                ),
                                dmc.Anchor(
                                    DashIconify(icon="mdi:web", height=25),
                                    href="https://hisqkq.github.io/", 
                                    target="_blank"
                                ),
                                dmc.Anchor(
                                    DashIconify(icon="mdi:email", height=25),
                                    href="mailto:theo33220@hotmail.com", 
                                    target="_blank"
                                )
                            ]
                        ),
                    ],
                    style={"margin": "auto"},
                ),
                # Carte de Baptiste Gerbouin
                dmc.Card(
                    withBorder=True,
                    shadow="sm",
                    radius="md",
                    w=450,
                    children=[
                        dmc.CardSection(
                            dmc.Image(
                                src="https://via.placeholder.com/350x160.png?text=Baptiste+Gerbouin",  # Remplacer par l'URL de l'image
                                h=250,
                                alt="Baptiste Gerbouin"
                            )
                        ),
                        dmc.Group(
                            justify="apart",
                            mt="md",
                            mb="xs",
                            children=[
                                dmc.Text("Baptiste Gerbouin", fw=500),
                            ]
                        ),
                        dmc.Text(
                            "Final-year CMI ISI student with a passion for machine learning and data analytics.",
                            size="sm",
                            c="dimmed"
                        ),
                        dmc.Space(h="sm"),
                        dmc.Text(
                            "Academic Background:",
                            fw=500,
                            size="sm"
                        ),
                        dmc.List(
                            [
                                dmc.ListItem("Licence & Master in CMI ISI, University of Bordeaux"),
                                dmc.ListItem("3rd year at Université Libre de Bruxelles, Belgium")
                            ],
                            size="xs",
                            c="dimmed"
                        ),
                        dmc.Space(h="sm"),
                        dmc.Text(
                            "Actually doing an internship at:",
                            fw=500,
                            size="sm"
                        ),
                        dmc.Text(
                            "Suez - Data Science & Machine Learning, Bordeaux",
                            size="sm",
                            c="dimmed"
                        ),
                        dmc.Group(
                            mt="md",
                            children=[
                                dmc.Anchor(
                                    DashIconify(icon="mdi:github", height=25),
                                    href="https://github.com/baptiste-gerbouin",  
                                    target="_blank"
                                ),
                                dmc.Anchor(
                                    DashIconify(icon="mdi:linkedin", height=25),
                                    href="https://www.linkedin.com/in/baptiste-gerbouin",  
                                    target="_blank"
                                ),
                                dmc.Anchor(
                                    DashIconify(icon="mdi:web", height=25),
                                    href="https://baptistegerbouin-portfolio.example.com",  # Remplacer par le portfolio
                                    target="_blank"
                                ),
                                dmc.Anchor(
                                    DashIconify(icon="mdi:email", height=25),
                                    href="mailto:baptiste.gerbouin@example.com",  
                                    target="_blank"
                                )
                            ]
                        ),
                    ],
                    style={"margin": "auto"},
                ),
            
            ],
            # On centre les deux cartes horizontalement
            style={"marginBottom": "2rem", "margin": "auto", "width": "80%"}
        ),
        dmc.Space(h="xl"),
    ],
    style={"padding": "1rem"}
)
