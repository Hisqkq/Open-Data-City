import dash
import dash_mantine_components as dmc
from dash import dcc, html, Input, Output, State, clientside_callback, _dash_renderer, callback

from components.header import header_component
from components.sidebar import sidebar_component

_dash_renderer._set_react_version("18.2.0")

external_scripts = ["https://cdn.plot.ly/plotly-latest.min.js"]

app = dash.Dash(__name__, use_pages=True, external_stylesheets=dmc.styles.ALL, external_scripts=external_scripts)

# 🟢 Layout principal avec MantineProvider mis à jour dynamiquement
app.layout = html.Div(
    [
        dcc.Store(id="theme-store", data="light"),  # Stocke le mode sombre/clair
        dcc.Store(id="sidebar-state", data=True),   # Stocke l'état de la sidebar
        dcc.Location(id="url"),

        dmc.MantineProvider(
            id="mantine-provider",
            theme={"colorScheme": "light"},  
            children=[
                header_component(),  # Header
                sidebar_component(),  # Sidebar
                dash.page_container,  # Contenu des pages
            ]
        )
    ]
)

# 🔄 Callback pour mettre à jour MantineProvider selon `theme-store`
@callback(
    Output("mantine-provider", "theme"),
    Input("theme-store", "data"),  # Écoute les changements de `theme-store`
    prevent_initial_call=True
)
def update_theme(theme):
    return {"colorScheme": theme}

# 🔄 Clientside Callback pour changer le mode sombre / clair
clientside_callback(
    """
    (n_clicks, currentTheme) => {
        let newTheme = currentTheme === 'light' ? 'dark' : 'light';
        document.documentElement.setAttribute('data-mantine-color-scheme', newTheme);
        return newTheme;
    }
    """,
    Output("theme-store", "data"),  # Mise à jour du `theme-store`
    [Input("theme-toggle", "n_clicks")],  # Bouton du header
    [State("theme-store", "data")],  # État actuel du thème
)

if __name__ == "__main__":
    app.run_server(debug=True)