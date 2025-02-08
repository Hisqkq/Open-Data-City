import dash_mantine_components as dmc
from dash import html, clientside_callback, Input, Output

def footer_component():
    return dmc.Paper(
        children=[
            dmc.Divider(variant="solid"),
            dmc.Space(h="md"),
            dmc.Group(
                justify="center",  # Ajoutez cette propriété pour centrer horizontalement
                align="center",
                style={"width": "100%"},
                children=[
                    # Texte et liens
                    html.Div(
                        children=[
                            dmc.Text(
                                "This project was developed in 2025 as part of the Open Data Project at the University of Bordeaux. We are two CMI ISI students in last year of study. The data used in this project is from the Singapore Open Data Website.",
                                size="sm"
                            ),
                            dmc.Space(h="xs"),
                            dmc.Group(
                                justify="center",
                                children=[
                                    dmc.Anchor("About Us", href="/about-us", underline=True),
                                    dmc.Text("|", size="sm"),
                                    dmc.Anchor("Singapore Open Data Website", href="https://data.gov.sg/", target="_blank", underline=True)
                                ],
                                style={"textAlign": "center"}
                            )
                        ],
                        style={"textAlign": "center"}
                    ),
                    # Logo de l'université avec lien
                    html.Div(
                        children=[
                            dmc.Anchor(
                                href="https://www.u-bordeaux.fr/",
                                target="_blank",
                                children=[
                                    html.Img(
                                        id="footer-logo",
                                        src="/assets/img/bordeaux_log.svg",
                                        style={"height": "40px"}  # Taille initiale
                                    )
                                ]
                            )
                        ],
                        style={"marginTop": "1rem", "marginBottom": "1rem", "textAlign": "center"},
                    )
                ]
            )
        ],
        withBorder=False,
        shadow="sm",
        style={
            "padding": "1rem",
            "marginTop": "2rem",
            "textAlign": "center"
        }
    )

# Clientside callback to invert the logo color in dark mode.
clientside_callback(
    """
    (theme) => {
        return theme === 'dark' ? {"filter": "invert(100%)", "height": "40px"} : {"filter": "invert(0%)", "height": "40px"};
    }
    """,
    Output("footer-logo", "style"),
    Input("theme-store", "data")
)
