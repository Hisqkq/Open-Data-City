import dash
import dash_mantine_components as dmc
from dash import dcc, html, Input, Output, State, clientside_callback, _dash_renderer, callback

from components.header import header_component
from components.sidebar import sidebar_component
from components.footer import footer_component

_dash_renderer._set_react_version("18.2.0")
dmc.add_figure_templates()

app = dash.Dash(__name__, use_pages=True, external_stylesheets=dmc.styles.ALL)

app.layout = html.Div(
    [
        dcc.Store(id="theme-store", data="dark"),  
        dcc.Store(id="sidebar-state", data=True),   
        dcc.Location(id="url"),

        dmc.MantineProvider(
            id="mantine-provider",
            theme={"colorScheme": "dark"},  
            children=[
                header_component(),  
                sidebar_component(),  
                dash.page_container, 
                footer_component(), 
            ]
        )
    ]
)

# 🔄 Callback to update the theme store
@callback(
    Output("mantine-provider", "theme"),
    Input("theme-store", "data"),  
    prevent_initial_call=True
)
def update_theme(theme):
    return {"colorScheme": theme}

# 🔄 clientside_callback to update the theme with the theme store
clientside_callback(
    """
    (n_clicks, currentTheme) => {
        let newTheme = currentTheme === 'light' ? 'dark' : 'light';
        document.documentElement.setAttribute('data-mantine-color-scheme', newTheme);
        return newTheme;
    }
    """,
    Output("theme-store", "data"),  
    [Input("theme-toggle", "n_clicks")], 
    [State("theme-store", "data")],  
)

server = app.server

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050)
