import plotly.express as px
import plotly.graph_objects as go
from dash import dash_table
from dash import html
from services.data.process_data_immo import process_data_immo, process_data_table_intro

def create_line_chart_figure_introduction():
    """
    Crée une figure Plotly Express (line chart) pour l'introduction.
    """
    df_agg = process_data_immo()
    
    fig = px.line(
        df_agg,
        x="Date",
        y="price_m2",
        title="Price per m2 depending on the date",
    )
    return fig

def create_table_figure_introduction():
    """
    Crée une table stylisée avec Dash pour l'introduction.
    """
    df_agg = process_data_table_intro()

    table = dash_table.DataTable(
        columns=[{"name": col, "id": col} for col in df_agg.columns],
        data=df_agg.to_dict("records"),
        style_table={"overflowX": "auto"},
        style_header={
            "backgroundColor": "#1E1E1E",  # Fond du header sombre
            "color": "white",
            "fontWeight": "bold",
            "textAlign": "center",
            "border": "1px solid #444",
        },
        style_cell={
            "backgroundColor": "#282828",  # Fond sombre pour les cellules
            "color": "white",
            "textAlign": "center",
            "padding": "10px",
            "border": "1px solid #444",
        },
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": "#333"},  # Alternance des lignes
            {"if": {"state": "selected"}, "backgroundColor": "#444"},  # Highlight au clic
        ],
    )

    return html.Div(table, style={"width": "80%", "margin": "auto", "padding": "20px"})






############################################
# creation map income + median salary
############################################


# Folium map

import folium
import json

def get_fill_color(price):
    """
    Retourne une couleur pour les polygones en fonction de la population.
    L'échelle va de light yellow (#ffffcc) pour de faibles valeurs à dark red (#800026) pour de fortes valeurs,
    sur une plage de 10 000 à 200 000.
    """
    min_price, max_price = 3000, 10000
    if price is None:
        return "#ffffff"
    norm = (price - min_price) / (max_price - min_price)
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

def create_folium_map(geojson_path="services/data/processed/PriceWithSalary.geojson"):
    """
    Crée une carte Folium qui affiche :
      - Les planning areas (polygones) colorées en fonction du prix au mètre carré.
      - Des cercles (CircleMarkers) positionnés sur le centroïde, dont la couleur et le rayon dépendent du salaire médian.
      - Deux légendes HTML indiquant respectivement l'échelle du prix au mètre carré et l'échelle de salaire médian.
    """
    # Charger le GeoJSON
    with open(geojson_path, "r", encoding="utf-8") as f:
        geojson = json.load(f)
    
    # Créer la carte centrée sur Singapore
    m = folium.Map(location=[1.3521, 103.8198], zoom_start=11)
    
    # Ajout des polygones avec style selon le prix au mètre carré
    def style_function(feature):
        price = feature["properties"].get("price_m2")
        return {
            "fillColor": get_fill_color(price),
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
     <b>Price Scale</b><br>
     3k - 5k: <i style="background:#ffffcc; width:20px; height:20px; display:inline-block"></i><br>
     5k - 7k: <i style="background:#fed976; width:20px; height:20px; display:inline-block"></i><br>
     7k - 9k: <i style="background:#fd8d3c; width:20px; height:20px; display:inline-block"></i><br>
     9k - 12k: <i style="background:#800026; width:20px; height:20px; display:inline-block"></i>
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
    m.save("folium_map_immo_price.html")