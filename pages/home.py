import dash
import dash_mantine_components as dmc

from dash_extensions import Lottie

dash.register_page(__name__, path="/")

layout = dmc.Container(
    children=[
        dmc.Title("Welcome to the Singapore's Open Data application.", order=1),
        dmc.Text("The goal of this application is to provide a simple and user-friendly interface to explore Singapore's open data."),
        Lottie(
            options=dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice')),
            width="35%", url="https://lottie.host/55f711be-705a-45f2-8f35-08456dcf6db0/8J4gG2IGrO.json"
        )
    ],
    fluid=True,
)
