import dash
import dash_mantine_components as dmc
from dash import html
from dash_extensions import Lottie

dash.register_page(__name__, path="/")

layout = dmc.Container(
    fluid=True,
    p="xl",
    children=[
        # Section d'introduction avec titre et description dans un Paper
        dmc.Paper(
            withBorder=True,
            shadow="md",
            radius="md",
            p="lg",
            mb="xl",
            children=[
                dmc.Title("Welcome to Singapore's Open Data Application", order=1),
                dmc.Space(h="sm"),
                dmc.Text(
                    "This application provides a simple and user-friendly interface to explore Singapore's open data. "
                    "Discover a variety of cool components and designs with Dash Mantine Components!",
                    size="lg",
                ),
            ],
        ),

        # Titre de la section Lotties
        dmc.Text("Cool Lotties we could use:", size="xl", mb="md"),

        # Grille 2x2 des animations Lottie avec SimpleGrid
        dmc.SimpleGrid(
            cols=2,
            spacing="md",
            children=[
                dmc.Card(
                    shadow="sm",
                    padding="lg",
                    radius="md",
                    withBorder=True,
                    children=Lottie(
                        options=dict(
                            loop=True,
                            autoplay=True,
                            rendererSettings=dict(preserveAspectRatio='xMidYMid slice'),
                        ),
                        width="100%",
                        url="https://lottie.host/55f711be-705a-45f2-8f35-08456dcf6db0/8J4gG2IGrO.json",
                    ),
                ),
                dmc.Card(
                    shadow="sm",
                    padding="lg",
                    radius="md",
                    withBorder=True,
                    children=Lottie(
                        options=dict(
                            loop=True,
                            autoplay=True,
                            rendererSettings=dict(preserveAspectRatio='xMidYMid slice'),
                        ),
                        width="100%",
                        url="https://lottie.host/fc97c53a-ff71-4ac8-b816-3e2305ab22b0/IHMrWokYqy.json",
                    ),
                ),
                dmc.Card(
                    shadow="sm",
                    padding="lg",
                    radius="md",
                    withBorder=True,
                    children=Lottie(
                        options=dict(
                            loop=True,
                            autoplay=True,
                            rendererSettings=dict(preserveAspectRatio='xMidYMid slice'),
                        ),
                        width="100%",
                        url="https://lottie.host/37863b94-0bbe-484e-8098-a29035fe778b/TFq8Yxmmds.json",
                    ),
                ),
                dmc.Card(
                    shadow="sm",
                    padding="lg",
                    radius="md",
                    withBorder=True,
                    children=Lottie(
                        options=dict(
                            loop=True,
                            autoplay=True,
                            rendererSettings=dict(preserveAspectRatio='xMidYMid slice'),
                        ),
                        width="100%",
                        url="https://lottie.host/79d4e32b-2ed7-4df2-b4a5-b5ead10bc2be/yosMzk6470.json",
                    ),
                ),
            ],
        ),

        # Espace et texte de footer pour conclure
        dmc.Space(h=30),
        dmc.Text(
            "Showcasing the possibilities of Dash Mantine Components",
            size="lg",
            style={"textAlign": "center"},
        ),
    ],
)
