import dash_mantine_components as dmc
from dash import html

def education_bar_chart():
    chart = dmc.BarChart(
        id="education-bar-chart",
        h=450,
        data=[],  # sera mis à jour via le callback
        dataKey="university",
        series=[{"name": "gross_salary"}],
        withLegend=False,
        unit=" S$",
        withTooltip=True,
        withXAxis=True,
        withYAxis=True,
        yAxisLabel="Gross Salary",
        xAxisProps={
            "tickMargin": 10,
            "interval": 0,    # Affiche tous les ticks
            "angle": -7      # Rotation des labels pour une meilleure lisibilité
        },
        barProps={
            "radius": 5,                # Applique un arrondi aux barres
            "isAnimationActive": True,  # Active l'animation
            "animationDuration": 800    # Durée de l'animation en ms
        },
        style={"marginTop": "1rem", "marginBottom": "1rem"}
    )
    
    reset_button = dmc.Button(
                    "Reset",
                    id="reset-btn",
                    variant="outline",
                    style={"position": "absolute", "top": "1px", "right": "1px"}
                )
    
    # Conteneur parent en position relative pour que le bouton soit positionné correctement
    container = html.Div(
        children=[chart, reset_button],
        style={"position": "relative"}
    )
    
    return container
