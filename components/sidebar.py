from dash import html, callback, Input, Output, State, dcc
import dash_mantine_components as dmc

from utils.icon import get_icon
from utils.config import NAV_LINKS

def sidebar_component():
    children = []
    
    # Ajout de l'élément Home en premier
    home = NAV_LINKS.get("Home")
    if home:
        children.append(
            dmc.NavLink(
                id="nav-Home",
                label="Home",
                leftSection=get_icon(home[1]),
                href=home[0],
                active=False
            )
        )
    
    # Séparateur
    children.append(dmc.Divider(m="sm"))
    
    # Parcourir les groupes (Topics et Other)
    for group_label, items in NAV_LINKS.items():
        if group_label == "Home":
            continue
        # Titre de groupe
        children.append(
            dmc.Text(group_label, fw=500, size="sm", style={"marginTop": "0.5rem", "marginBottom": "0.5rem"})
        )
        # Pour chaque élément du groupe
        for name, values in items.items():
            children.append(
                dmc.NavLink(
                    id=f"nav-{name}",
                    label=name,
                    leftSection=get_icon(values[1]),
                    href=values[0],
                    active=False
                )
            )
        # Ajouter un espace entre les groupes
        children.append(dmc.Space(h="sm"))
        children.append(dmc.Divider(m="sm"))
    
    return dmc.Drawer(
        id="sidebar",
        title="Navigation",
        padding="md",
        size="300px",
        opened=False,
        position="left",
        withCloseButton=True,
        children=children,
        style={"zIndex": 1000},
    )

# Callback pour ouvrir/fermer la sidebar
@callback(
    Output("sidebar", "opened"),
    Input("toggle-sidebar", "n_clicks"),
    State("sidebar", "opened"),
    prevent_initial_call=True
)
def toggle_sidebar(n_clicks, is_opened):
    return not is_opened

# Callback pour mettre à jour l'état actif des liens
@callback(
    [Output(f"nav-{name}", "active") for group in NAV_LINKS.values() 
     if isinstance(group, dict) for name in group.keys()] +
    [Output("nav-Home", "active")],
    Input("url", "pathname"),
)
def update_nav_links(current_path):
    outputs = []
    # Parcourir les liens dans les groupes (Topics et Other)
    for group in NAV_LINKS.values():
        if isinstance(group, dict):
            for values in group.values():
                outputs.append(current_path == values[0])
    # Ajouter la vérification pour Home
    outputs.append(current_path == NAV_LINKS["Home"][0])
    return outputs
