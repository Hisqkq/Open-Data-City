import dash
from dash import html, Input, Output, dcc, callback
import dash_mantine_components as dmc

dash.register_page(__name__, path="/data")

layout = dmc.Container(
    children=[
        dmc.Title("Open Data Table", order=1, style={"marginBottom": "1rem"}),
    
        dmc.Table(
            striped=True,
            highlightOnHover=True,
            withColumnBorders=True,
            data={
                "caption": "Some elements from periodic table",
                "head": ["Element position", "Atomic mass", "Symbol", "Element name"],
                "body": [
                    [6, 12.011, "C", "Carbon"],
                    [7, 14.007, "N", "Nitrogen"],
                    [39, 88.906, "Y", "Yttrium"],
                    [56, 137.33, "Ba", "Barium"],
                    [58, 140.12, "Ce", "Cerium"],
                ],
            },
        )
    ],
    fluid=True,
    style={"padding": "1rem"},
)
