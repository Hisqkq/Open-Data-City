import plotly.graph_objects as go
import pandas as pd
import json
import dash_mantine_components as dmc

import dash_leaflet as dl
from dash import html

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

# Folium map

import folium
import json

def get_fill_color(pop):
    """
    Retourne une couleur pour les polygones en fonction de la population.
    L'échelle va de light yellow (#ffffcc) pour de faibles valeurs à dark red (#800026) pour de fortes valeurs,
    sur une plage de 10 000 à 200 000.
    """
    min_pop, max_pop = 10000, 200000  
    if pop is None:
        return "#ffffff"
    norm = (pop - min_pop) / (max_pop - min_pop)
    norm = max(0, min(1, norm))
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    def rgb_to_hex(rgb):
        return "#%02x%02x%02x" % rgb
    color1 = hex_to_rgb("#ffffcc")  # light yellow
    color2 = hex_to_rgb("#800026")  # dark red
    rgb = tuple(int(color1[i] + norm * (color2[i] - color1[i])) for i in range(3))
    return rgb_to_hex(rgb)

def parse_median_salary(category):
    """
    Tente d'extraire une valeur numérique représentant le salaire médian à partir d'une chaîne.
    Par exemple, "4_000_4_999" sera transformé en 4500.
    Si la chaîne contient "andOver", on extrait les chiffres.
    """
    try:
        if "andOver" in category:
            digits = "".join(filter(str.isdigit, category))
            return float(digits)
        else:
            parts = category.split("_")
            if len(parts) >= 2:
                low = float("".join(parts[:2]))
                if len(parts) > 2:
                    high = float("".join(parts[2:]))
                else:
                    high = low
                return (low + high) / 2
    except Exception:
        return None

def get_salary_color(salary):
    """
    Retourne une couleur pour le marker en fonction du salaire médian (valeur numérique).
    L'échelle va de light blue pour 3000 à light pink pour 12000.
    """
    min_sal, max_sal = 3000, 12000
    if salary is None:
        return "#808080"
    norm = (salary - min_sal) / (max_sal - min_sal)
    norm = max(0, min(1, norm))
    # Interpolation entre light blue (#ADD8E6) et light pink (#FFB6C1)
    r = int(173 + norm * (255 - 173))
    g = int(216 + norm * (182 - 216))
    b = int(230 + norm * (193 - 230))
    return f"#{r:02x}{g:02x}{b:02x}"

def get_marker_radius_for_salary(salary):
    """
    Calcule le rayon du marker en fonction de la valeur numérique du salaire médian.
    On attribue un rayon linéaire entre 5 et 20 pixels.
    """
    min_sal, max_sal = 3000, 12000
    min_radius, max_radius = 5, 20
    if salary is None:
        return min_radius
    norm = (salary - min_sal) / (max_sal - min_sal)
    norm = max(0, min(1, norm))
    return min_radius + norm * (max_radius - min_radius)

def create_folium_map(geojson_path="services/data/processed/PlanningAreaWithSalary.geojson"):
    """
    Crée une carte Folium qui affiche :
      - Les planning areas (polygones) colorées en fonction de la population.
      - Des cercles (CircleMarkers) positionnés sur le centroïde, dont la couleur et le rayon dépendent du salaire médian.
      - Deux légendes HTML indiquant respectivement l'échelle de population et l'échelle de salaire médian.
    """
    # Charger le GeoJSON
    with open(geojson_path, "r", encoding="utf-8") as f:
        geojson = json.load(f)
    
    # Créer la carte centrée sur Singapore
    m = folium.Map(location=[1.3521, 103.8198], zoom_start=11)
    
    # Ajout des polygones avec style selon la population
    def style_function(feature):
        pop = feature["properties"].get("working_population")
        return {
            "fillColor": get_fill_color(pop),
            "color": "black",
            "weight": 1,
            "fillOpacity": 0.7
        }
    
    folium.GeoJson(
        geojson,
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(fields=["PLN_AREA_N"], aliases=["Area:"])
    ).add_to(m)
    
    # Ajout des cercles pour les salaires
    for feature in geojson["features"]:
        pop = feature["properties"].get("working_population")
        if pop is None or pop <= 0:
            continue
        centroid = feature["properties"].get("centroid")
        if not centroid:
            continue
        salary_cat = feature["properties"].get("median_salary_category")
        salary_value = parse_median_salary(salary_cat)
        marker_color = get_salary_color(salary_value)
        marker_radius = get_marker_radius_for_salary(salary_value)
        folium.CircleMarker(
            location=[centroid["lat"], centroid["lng"]],
            radius=marker_radius,
            color="black",
            fill=True,
            fill_color=marker_color,
            fill_opacity=0.9,
            popup=folium.Popup(f"""
                <h4>{feature["properties"].get("PLN_AREA_N", "")}</h4>
                <p>Working Population: {pop}</p>
                <p>Median Salary: {salary_value if salary_value is not None else 'N/A'}</p>
            """, max_width=250)
        ).add_to(m)
    
    # Légende pour la population (polygones)
    population_legend = '''
     <div style="
     position: fixed; 
     bottom: 50px; left: 50px; width: 180px; height: 140px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color: white;
     opacity: 0.8;
     padding: 10px;
     ">
     <b>Population Scale</b><br>
     10k - 50k: <i style="background:#ffffcc; width:20px; height:20px; display:inline-block"></i><br>
     50k - 100k: <i style="background:#fed976; width:20px; height:20px; display:inline-block"></i><br>
     100k - 150k: <i style="background:#fd8d3c; width:20px; height:20px; display:inline-block"></i><br>
     150k - 200k: <i style="background:#800026; width:20px; height:20px; display:inline-block"></i>
     </div>
     '''
    m.get_root().html.add_child(folium.Element(population_legend))
    
    # Légende pour la médiane du salaire
    salary_legend = '''
     <div style="
     position: fixed; 
     bottom: 50px; right: 50px; width: 200px; height: 140px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color: white;
     opacity: 0.8;
     padding: 10px;
     ">
     <b>Median Salary Scale</b><br>
     3000 - 5000: <i style="background:#add8e6; width:20px; height:20px; display:inline-block"></i><br>
     5000 - 7000: <i style="background:#c4a3d2; width:20px; height:20px; display:inline-block"></i><br>
     7000 - 9000: <i style="background:#e498a6; width:20px; height:20px; display:inline-block"></i><br>
     9000 - 12000: <i style="background:#ffb6c1; width:20px; height:20px; display:inline-block"></i>
     </div>
     '''
    m.get_root().html.add_child(folium.Element(salary_legend))
    
    return m

if __name__ == "__main__":
    m = create_folium_map()
    m.save("folium_map.html")
