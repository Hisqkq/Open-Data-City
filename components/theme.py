from dash import Input, Output, ctx
import dash_mantine_components as dmc
from dash_iconify import DashIconify


def get_icon(icon, height=20):
    return DashIconify(icon=icon, height=height)


# Stockage du thème dans dcc.Store
def get_theme_store():
    return dmc.MantineProvider(theme={"colorScheme": "light"})


# Callback pour gérer le changement de thème
def get_theme_callback(app):
    @app.callback(
        Output("theme-store", "data"),
        Output("theme-toggle", "children"),
        [Input("theme-toggle", "n_clicks")],
        prevent_initial_call=True
    )
    def toggle_theme(n_theme):
        current_theme = app.layout.children[0].data
        new_theme = "dark" if current_theme == "light" else "light"
        new_icon = get_icon("tabler:sun") if new_theme == "dark" else get_icon("tabler:moon")
        return new_theme, new_icon
