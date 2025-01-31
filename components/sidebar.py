from dash import html, callback, Input, Output, State, dcc
import dash_mantine_components as dmc

from utils.icon import get_icon
from utils.config import NAV_LINKS

# 🟢 Sidebar Component (Drawer rétractable)
def sidebar_component():
    return dmc.Drawer(
        id="sidebar",
        title="Navigation",
        padding="md",
        size="300px",  
        opened=False,  
        position="left",
        withCloseButton=True,  
        children=[
            dmc.NavLink(
                id=f"nav-{name}",
                label=name,
                leftSection=get_icon(values[1]),  # Récupération correcte de l'icône
                href=values[0],  # Récupération correcte de l'URL
                active=False
            )
            for name, values in NAV_LINKS.items()
        ],
    )

# 🔄 Callback pour ouvrir/fermer la sidebar
@callback(
    Output("sidebar", "opened"),  
    Input("toggle-sidebar", "n_clicks"), 
    State("sidebar", "opened"),  
    prevent_initial_call=True
)
def toggle_sidebar(n_clicks, is_opened):
    return not is_opened  

# 🔄 Callback pour mettre à jour `active` des `NavLink`
@callback(
    [Output(f"nav-{name}", "active") for name in NAV_LINKS.keys()],  # Mise à jour dynamique
    Input("url", "pathname"),  # Écoute l'URL actuelle
)
def update_nav_links(current_path):
    return [current_path == values[0] for values in NAV_LINKS.values()]  # Active uniquement le bon lien
