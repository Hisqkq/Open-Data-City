import dash
import dash_mantine_components as dmc
from dash import html, dcc
from dash_iconify import DashIconify

dash.register_page(__name__, path="/")

layout = dmc.Container(
    fluid=True,
    p="xl",
    children=[
        # Titre principal
        dmc.Group(
            align="center",
            justify="center",
            children=[
                dmc.Title("Welcome to Singapore Open Data", order=1)
            ],
            style={"marginBottom": "1rem"}
        ),
        dmc.Text(
            "Explore our interactive insights on key themes in Singapore: Education, Housing, and Economy.",
            size="lg",
            style={"marginBottom": "2rem", "textAlign": "center"}
        ),
        # Cartes des thèmes
        dmc.SimpleGrid(
            cols=3,
            spacing="lg",
            children=[
                # Carte Education
                dcc.Link(
                    dmc.Card(
                        className="hover-card",
                        withBorder=True,
                        shadow="sm",
                        radius="md",
                        p="xl",
                        children=[
                            DashIconify(icon="tabler:book", height=40, color="#228be6"),
                            dmc.Title("Education", order=3, style={"textAlign": "center"}),
                            dmc.Text(
                                "Discover insights and trends in Singapore's education system.",
                                size="sm",
                                style={"textAlign": "center"}
                            )
                        ]
                    ),
                    href="/education"
                ),
                # Carte Housing
                dcc.Link(
                    dmc.Card(
                        className="hover-card",
                        withBorder=True,
                        shadow="sm",
                        radius="md",
                        p="xl",
                        children=[
                            DashIconify(icon="tabler:home", height=40, color="#ff7f0e"),
                            dmc.Title("Housing", order=3, style={"textAlign": "center"}),
                            dmc.Text(
                                "Explore data on housing prices and demographics in Singapore.",
                                size="sm",
                                style={"textAlign": "center"}
                            )
                        ]
                    ),
                    href="/housing"
                ),
                # Carte Economy
                dcc.Link(
                    dmc.Card(
                        className="hover-card",
                        withBorder=True,
                        shadow="sm",
                        radius="md",
                        p="xl",
                        children=[
                            DashIconify(icon="tabler:chart-bar", height=40, color="#2ca02c"),
                            dmc.Title("Economy", order=3, style={"textAlign": "center"}),
                            dmc.Text(
                                "Analyze economic indicators and market trends in Singapore.",
                                size="sm",
                                style={"textAlign": "center"}
                            )
                        ]
                    ),
                    href="/economy"
                ),
            ]
        )
    ],
    style={"padding": "1rem"}
)
