import plotly.graph_objects as go
import pandas as pd
import dash_mantine_components as dmc
from services.data.process_economic_data import get_unemployment_by_city, get_overall_unemployment_rate, get_unemployment_by_age, get_unemployment_by_qualification, get_unemployment_by_sex

def create_unemployment_bar_chart(theme="mantine_light"):
    """
    Crée un bar chart personnalisé avec Plotly Graph Objects pour le taux de chômage par ville.
    
    - Singapore est affiché en bleu clair (#ADD8E6).
    - Hong Kong en bleu foncé (#00008B).
    - Los Angeles et Paris en rouge (#FF0000).
    - Le reste en vert (#008000).
    
    Les barres ont un contour blanc pour une apparence adoucie (remarque : Plotly ne propose pas d'arrondi natif).
    
    Paramètres:
      - theme: Template Plotly, par exemple "mantine_light" ou "mantine_dark".
      
    Retourne:
      - Une figure Plotly.
    """
    # Charger les données (supposons que la fonction get_unemployment_by_city renvoie un DataFrame)
    df = get_unemployment_by_city()  # DataFrame avec colonnes : Year, City, Unemployment Rate
    
    # Définir la palette de couleurs spécifique
    color_map = {
        "Singapore": "#A7C7E7",   # pastel light blue
        "Tokyo": "#5A5D9D",   # pastel dark blue
        "Los Angeles": "#C84C4C", # slightly darker pastel red
        "Paris": "#C84C4C",        # slightly darker pastel red
        "London": "#E57373",       # pastel red
        "New York": "#E57373",     # pastel red
    }

    default_color = "#008000"  # green pour les autres villes
    
    # Appliquer la couleur à chaque ville
    colors = [color_map.get(city, default_color) for city in df["City"]]
    
    # Créer le bar chart
    fig = go.Figure(layout=dict(barcornerradius=15),
        data=go.Bar(
            x=df["City"],
            y=df["Unemployment Rate"],
            marker=dict(
                color=colors,
                line=dict(color="white", width=1)  # contour blanc pour adoucir l'aspect
            ),
            opacity=0.8,
        )
    )
    
    # Mettre à jour le layout
    fig.update_layout(
        title="Unemployment Rate by City (2024)",
        xaxis_title="City",
        yaxis_title="Unemployment Rate (%)",
        template=theme,
        margin=dict(l=50, r=50, t=80, b=50),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        ),
        hovermode="x unified",
    )

    fig.update_xaxes(showspikes=False)
    

    # Ajout d'une barre verticale bleue à 3% pour indiquer un seuil
    fig.add_shape(
        type="line",
        x0=-0.5,
        x1=len(df["City"]) - 0.5,
        y0=2.5,
        y1=2.5,
        line=dict(color="#5A5D9D", width=2, dash="dash"),
    )

    fig.add_shape(
        type="line",
        x0=-0.5,
        x1=len(df["City"]) - 0.5,
        y0=5,
        y1=5,
        line=dict(color="#E57373", width=2, dash="dash"),
    )

    return fig


def create_overal_unemployment_line():
    """
    Crée un line chart personnalisé avec Plotly Graph Objects pour le taux de chômage global.
    
    Paramètres:
      - Aucun.
      
    Retourne:
      - Une figure Plotly.
    """
    # Charger les données (supposons que la fonction get_overall_unemployment_rate renvoie un DataFrame)
    data = get_overall_unemployment_rate()  # DataFrame avec colonnes : Year, Unemployment Rate

    return dmc.LineChart(
        h=300,
        data=data,
        series=[{"name": "unemployment_rate", "label": "Unemployment Rate"}],
        dataKey="year",
        type="gradient",
        strokeWidth=5,
        curveType="natural",
        yAxisProps={"domain": [1.0, 5.0]},  # Ajusté en fonction de la plage du taux de chômage
        p="lg",
        withLegend=True,
        tooltipAnimationDuration=200,
        unit="%",
    )


def create_unemployment_residents_line_chart(category="Qualification"):
    """
    Creates a dmc.LineChart displaying unemployment rates by year,
    with discrete colors assigned to each series.

    Parameters:
      - category: one of "Age", "Qualification", "Sex". 
          * "Age" uses the CSV unemployment_by_age.csv,
          * "Qualification" uses the CSV unemployment_by_qualification.csv,
          * "Sex" uses the CSV unemployment_by_sex.csv.
      - template: Mantine template (e.g., "mantine_light" or "mantine_dark").

    Returns:
      - A dmc.LineChart with data pivoted so that each row corresponds to a year
        and each column (except "year") corresponds to a group, with discrete colors.
    """
    # Mapping des chemins CSV
    csv_paths = {
        "Age": "services/data/raw/annual average resident unemployment rate by age.csv",
        "Qualification": "services/data/raw/annual average resident unemployment rate by HQA.csv",
        "Sex": "services/data/raw/annual average resident unemployment rate by sex.csv"
    }
    
    # Récupérer les données selon la catégorie sélectionnée
    if category == "Age":
        data = get_unemployment_by_age(csv_paths["Age"])
    elif category == "Qualification":
        data = get_unemployment_by_qualification(csv_paths["Qualification"])
    elif category == "Sex":
        data = get_unemployment_by_sex(csv_paths["Sex"])
    else:
        data = []
    
    dataKey = "year"
    
    series = []
    if data:
        keys = [key for key in data[0].keys() if key != "year"]
        # Palette de couleurs discrètes
        color_palette = ["pink.6", "blue.6", "teal.6", "orange.6", "red.6", "green.6", "cyan.6", "violet.6", "lime.6", "indigo.6", "amber.6", "purple.6", "yellow.6", "gray.6"]
        for i, key in enumerate(keys):
            series.append({
                "name": key,
                "label": key,
                "color": color_palette[i % len(color_palette)]
            })
    
    domain = [0, 10]  

    return dmc.LineChart(
        h=300,
        data=data,
        series=series,
        dataKey=dataKey,
        type="default",  # Utilise le type par défaut (non gradient)
        strokeWidth=5,
        curveType="natural",
        p="lg",
        withLegend=True,
        tooltipAnimationDuration=200,
        unit="%",
    )

