import dash_mantine_components as dmc
from dash import html, dcc, clientside_callback, callback, Output, Input
from utils.icon import get_icon
from utils.config import GITHUB_LINK, NAV_LINKS
from dash_iconify import DashIconify
from dash_mantine_components import Select

# Construction de la liste des options à partir de NAV_LINKS
options = [{"value": values[0], "label": name} for name, values in NAV_LINKS.items()]

search_select = Select(
    id="nav-search-select",
    data=options,
    placeholder="Search for a page...",
    searchable=True,
    nothingFoundMessage="Nothing found...",
    leftSection=DashIconify(icon="tabler:search"),
    rightSection=dmc.Kbd("⌘ + k", style={"display": "inline-block", "whiteSpace": "nowrap"}),
    rightSectionWidth=60,
    style={"minWidth": "300px"}
)

def header_component():
    return dmc.Paper(
        children=[
            dmc.Group(
                children=[
                    # Left side group: Sidebar toggle, search select, and logo + title
                    dmc.Group(
                        children=[
                            dmc.ActionIcon(
                                id="toggle-sidebar",
                                children=get_icon("tabler:menu-2", height=22),
                                variant="filled",
                                color="gray",
                                size="lg",
                                style={
                                    "margin": "0.5rem",
                                    "transition": "0.3s ease-in-out",
                                },
                            ),
                            # Groupe pour le logo et le titre
                            dmc.Group(
                                children=[
                                    dcc.Link(
                                        html.Img(
                                            id="header-logo",
                                            src="/assets/img/lion-logo.png",
                                            style={"height": "40px"},  # Taille du logo
                                        ),
                                        href="/",
                                        style={"textDecoration": "none"},
                                    ),
                                    dcc.Link(
                                        html.Span(
                                            [
                                                html.Span("Singapore", id="title-singapore", style={"fontWeight": "bold", "color": "#212529"}),
                                                html.Span("’s Open Data", id="title-open-data", style={"fontWeight": "lighter", "color": "#868e96"}),
                                            ],
                                            id="header-title",
                                            style={
                                                "fontSize": "1.5rem",
                                                "display": "flex",
                                                "alignItems": "center",
                                                "marginLeft": "0.5rem"  # Décalage pour aligner légèrement le titre à gauche
                                            },
                                        ),
                                        href="/",
                                        style={"textDecoration": "none"},
                                    ),
                                ],
                                align="center",
                                style={"marginLeft": "1rem"}
                            ),
                        ],
                        align="center"
                    ),
                    # Right side group: Boutons GitHub et thème
                    dmc.Group(
                        children=[
                            search_select,
                            dmc.Anchor(
                                dmc.ActionIcon(get_icon("mdi:github", height=25), variant="subtle", size="lg"),
                                href=GITHUB_LINK,
                                target="_blank"
                            ),
                            dmc.ActionIcon(
                                id="theme-toggle",
                                children=get_icon("tabler:moon", height=25),
                                variant="subtle",
                                size="lg",
                            ),
                        ],
                        align="right"
                    ),
                ],
                justify="space-between",
                align="center",
                style={"padding": "0.5rem 1rem"}
            )
        ],
        shadow="sm",
        withBorder=True,
        style={
            "padding": "0.5rem 1rem",
            "position": "sticky",
            "top": "0",
            "zIndex": "100",
            "width": "100%"
        },
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

# 🔄 Callback pour changer de page avec le select 
@callback(
    Output("url", "pathname"),
    Input("nav-search-select", "value"),
    prevent_initial_call=True
)
def change_page(value):
    return value