import dash_mantine_components as dmc
from dash import html, dcc, clientside_callback, callback, Output, Input
from utils.icon import get_icon
from utils.config import GITHUB_LINK

# 🟢 Header Component
def header_component():
    return dmc.Paper(
        children=[
            dmc.Group(
                [
                    # 📌 Bouton pour ouvrir/fermer la Sidebar
                    dmc.ActionIcon(
                        id="toggle-sidebar",
                        children=get_icon("tabler:menu-2", height=22),
                        variant="filled",  # 🔥 Amélioration : Bouton rempli
                        color="gray",  # 🔥 Amélioration : Couleur neutre
                        size="lg",
                        style={
                            "margin": "0.5rem",
                            "transition": "0.3s ease-in-out",
                        },
                    ),

                    # 📌 Logo + Titre
                    dmc.Group(
                        [
                            # 🔵 Logo de Singapour avec inversion en mode sombre
                            html.Img(
                                id="header-logo",
                                src="/assets/img/lion-logo.png",
                                style={"height": "3px"},  # 🔥 Réduction de la taille
                            ),

                            # 🔵 Titre stylisé avec ID pour mise à jour dynamique
                            html.Span(
                                [
                                    html.Span("Singapore", id="title-singapore", style={"fontWeight": "bold", "color": "#212529"}),
                                    html.Span("’s Open Data", id="title-open-data", style={"fontWeight": "lighter", "color": "#868e96"}),
                                ],
                                id="header-title",
                                style={"fontSize": "1.5rem", "display": "flex", "alignItems": "center"},
                            ),
                        ],
                        align="center",
                    ),

                    # 🌙 Boutons (GitHub + Thème sombre/claire)
                    dmc.Group(
                        [
                            # 🖥 Lien GitHub
                            dmc.Anchor(
                                dmc.ActionIcon(get_icon("mdi:github", height=25), variant="subtle", size="lg"),
                                href=GITHUB_LINK,
                                target="_blank"
                            ),
                            # 🌙 Bouton mode sombre/claire
                            dmc.ActionIcon(
                                id="theme-toggle",
                                children=get_icon("tabler:moon", height=25),
                                variant="subtle",
                                size="lg",
                            ),
                        ],
                        align="right",
                    ),
                ],
                justify="space-between",
                align="center",
                style={"padding": "0.5rem 1rem"},
            )
        ],
        shadow="sm",
        withBorder=True,
        style={"padding": "0.5rem 1rem"},
    )

# 🔄 Clientside Callback pour changer la couleur du logo en fonction du thème
clientside_callback(
    """
    (theme) => {
        return theme === 'dark' ? {"filter": "invert(100%)", "height": "40px"} : {"filter": "invert(0%)", "height": "40px"};
    }
    """,
    Output("header-logo", "style"),
    Input("theme-store", "data"),
)

# 🔄 Clientside Callback pour changer la couleur du titre en fonction du thème
clientside_callback(
    """
    (theme) => {
        return theme === 'dark' ? {"color": "#f1f3f5"} : {"color": "#212529"};
    }
    """,
    Output("title-singapore", "style"),
    Input("theme-store", "data"),
)

clientside_callback(
    """
    (theme) => {
        return theme === 'dark' ? {"color": "#adb5bd"} : {"color": "#868e96"};
    }
    """,
    Output("title-open-data", "style"),
    Input("theme-store", "data"),
)

# 🔄 Clientside Callback pour adapter le bouton sidebar selon le thème
clientside_callback(
    """
    (theme) => {
        return theme === 'dark' ? {"backgroundColor": "#495057", "color": "#f8f9fa", "transition": "0.3s"} 
                                : {"backgroundColor": "#dee2e6", "color": "#212529", "transition": "0.3s"};
    }
    """,
    Output("toggle-sidebar", "style"),
    Input("theme-store", "data"),
)

# 🔄 Callback Python pour mettre à jour l'icône du bouton (Lune 🌙 / Soleil ☀)
@callback(
    Output("theme-toggle", "children"),
    Input("theme-store", "data"),
    prevent_initial_call=True
)
def update_icon(theme):
    return get_icon("radix-icons:sun", height=25) if theme == "dark" else get_icon("radix-icons:moon", height=25)