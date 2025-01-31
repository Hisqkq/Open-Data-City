import dash_mantine_components as dmc

from utils.icon import get_icon

from utils.config import GITHUB_LINK

# 🟢 Header Component
def header_component():
    return dmc.Paper(
        children=[
            dmc.Group(
                [   # Bouton pour ouvrir/fermer la Sidebar
                    dmc.ActionIcon(
                        id="toggle-sidebar",
                        children=dmc.ThemeIcon(get_icon("tabler:menu-2"), size="lg"),
                        variant="subtle",
                        size="lg",
                        style={"margin": "0.5rem"}
                    ),
                    # 📌 Nom du projet
                    dmc.Text("Opendata Singapore", size="xl", style={"fontWeight": 700}),

                    # 🌙 Boutons 
                    dmc.Group(
                        [
                            # 🖥 Lien GitHub
                            dmc.Anchor(
                                dmc.ActionIcon(get_icon("mdi:github"), variant="subtle", size="lg"),
                                href=GITHUB_LINK,
                                target="_blank"
                            ),
                            # 🌙 Bouton mode sombre/claire
                            dmc.ActionIcon(
                                id="theme-toggle",
                                children=get_icon("tabler:moon"),
                                variant="subtle",
                                size="lg",
                            ),
                        ],
                        align="right",
                        style={"margin": "0", "padding": "0", "display": "flex", "gap": "1rem"},
                    ),
                ],
                justify="space-between",
                align="center",
            )
        ],
        shadow="sm",
        withBorder=True,
        style={"padding": "0.5rem 1rem"},
    )
