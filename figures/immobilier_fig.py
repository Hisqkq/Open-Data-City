import plotly.express as px
import plotly.graph_objects as go
from dash import dash_table
from dash import html
import folium
import json
import dash_mantine_components as dmc
import pandas as pd

from services.data.process_data_immo import process_data_immo, process_data_table_intro, process_data_line_history


import dash_mantine_components as dmc

def create_line_chart_figure_introduction():
    """
    Crée un line chart personnalisé avec Plotly Graph Objects pour la hausse des prix au mètre carré.
    """
    data_list = process_data_immo()  # Récupérer les données sous forme de dictionnaire

    return dmc.LineChart(
        h=300,
        data=data_list,
        series=[{"name": "price_m2", "label": "Price per m2"}],
        dataKey="Date",
        type="gradient",
        strokeWidth=5,
        curveType="natural",
        yAxisProps={"domain": [4500.0, 7200.0]},  # Ajusté en fonction de la plage du prix
        p="lg",
        withLegend=True,
        tooltipAnimationDuration=200,
        unit=" SGD",
    )



# def create_line_chart_figure_introduction():
#     """
#     Crée une figure Plotly Express (line chart) pour l'introduction.
#     """
#     df_agg = process_data_immo()
    
#     fig = px.line(
#         df_agg,
#         x="Date",
#         y="price_m2",
#         title="Price per m2 depending on the date",
#     )
#     return fig

import dash_mantine_components as dmc

def create_table_figure_introduction():
    """
    Crée une table stylisée avec Dash Mantine Components pour l'introduction.
    """
    data = process_data_table_intro()  # Assurez-vous que cette fonction renvoie une liste de dictionnaires
    
    # Création des lignes
    rows = [
        dmc.TableTr([dmc.TableTd(entry["Year"]), dmc.TableTd(entry["count"])])
        for entry in data
    ]
    
    # Création de l'en-tête
    head = dmc.TableThead(
        dmc.TableTr([dmc.TableTh("Year"), dmc.TableTh("Count")])
    )
    
    # Corps de la table
    body = dmc.TableTbody(rows)
    
    # Table complète avec style
    return dmc.Table(
        [head, body],
        withColumnBorders=True,
        highlightOnHover=True,
        striped=True,
        horizontalSpacing="md",
        verticalSpacing="sm",
        withTableBorder=True,
    )






##########################################
# CREATION DES MAPS SWITCH
##########################################

##########################################
# PREMIERE MAP
##########################################


def parse_median_salary(category):
    """
    Convertit une catégorie de salaire en valeur numérique médiane.
    Exemple : "4_000_4_999" devient 4500.
    """
    try:
        if "andOver" in category:
            digits = "".join(filter(str.isdigit, category))
            return float(digits)
        else:
            parts = category.split("_")
            if len(parts) >= 2:
                low = float("".join(parts[:2]))
                high = float("".join(parts[2:])) if len(parts) > 2 else low
                return (low + high) / 2
    except Exception:
        return None

def get_salary_color(salary):
    """
    Détermine la couleur du marqueur en fonction du salaire médian.
    """
    min_sal, max_sal = 3000, 12000
    if salary is None:
        return "#808080"  # Gris si inconnu
    norm = (salary - min_sal) / (max_sal - min_sal)
    norm = max(0, min(1, norm))
    r = int(173 + norm * (255 - 173))
    g = int(216 + norm * (182 - 216))
    b = int(230 + norm * (193 - 230))
    return f"#{r:02x}{g:02x}{b:02x}"


def get_fill_color(price):
    """
    Retourne une couleur pour les polygones en fonction du prix au mètre carré.
    L'échelle va de light yellow (#ffffcc) pour les faibles valeurs à dark red (#800026) pour les fortes valeurs.
    """
    min_price, max_price = 3000, 10000
    if price is None:
        return "#ffffff"
    
    norm = (price - min_price) / (max_price - min_price)
    norm = max(0, min(1, norm))  # Assurer que la valeur est entre 0 et 1

    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(rgb):
        return "#%02x%02x%02x" % rgb

    color1 = hex_to_rgb("#ffffcc")  # light yellow
    color2 = hex_to_rgb("#800026")  # dark red
    rgb = tuple(int(color1[i] + norm * (color2[i] - color1[i])) for i in range(3))
    
    return rgb_to_hex(rgb)

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


def create_folium_map(geojson_path="services/data/processed/PriceWithSalaryUpdated.geojson"):
    """
    Crée une carte Folium affichant :
      - Les planning areas colorées selon le prix au mètre carré.
      - Des marqueurs positionnés sur le centroïde de chaque zone avec info sur le prix/m² et les revenus médians.
      - Une légende indiquant l'échelle des prix/m².
    """
    # Charger le GeoJSON
    with open(geojson_path, "r", encoding="utf-8") as f:
        geojson = json.load(f)

    # Créer la carte centrée sur Singapore
    m = folium.Map(location=[1.3521, 103.8198], zoom_start=11)

    # Style des polygones en fonction du prix/m²
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
        tooltip=folium.GeoJsonTooltip(fields=["PLN_AREA_N", "price_m2"], aliases=["Area:", "Price/m²:"])
    ).add_to(m)


    # Ajout des cercles pour les salaires
    for feature in geojson["features"]:
        price = feature["properties"].get("price_m2")
        median_salary = feature["properties"].get("median_salary_category", "N/A")
        if price is None or price <= 0:
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
                <p>Working Population: {price}</p>
                <p>Median Salary: {salary_value if salary_value is not None else 'N/A'}</p>
            """, max_width=250)
        ).add_to(m)

    # Légende pour le prix/m²
    price_legend = '''
     <div style="position: fixed; bottom: 50px; left: 50px; width: 180px; height: 140px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color: white; opacity: 0.8; padding: 10px;">
     <b>Price m_2</b><br>
     3k - 5k: <i style="background:#ffffcc; width:20px; height:20px; display:inline-block"></i><br>
     5k - 7k: <i style="background:#fed976; width:20px; height:20px; display:inline-block"></i><br>
     7k - 9k: <i style="background:#fd8d3c; width:20px; height:20px; display:inline-block"></i><br>
     9k - 10k+: <i style="background:#800026; width:20px; height:20px; display:inline-block"></i>
     </div>
     '''
    m.get_root().html.add_child(folium.Element(price_legend))

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

# if __name__ == "__main__":
#     m = create_folium_map()
#     m.save("folium_map_price.html")


##########################################
# DEUXIEME MAP
##########################################



def parse_median_salary(category):
    """
    Convertit une catégorie de salaire en valeur numérique médiane.
    Exemple : "4_000_4_999" devient 4500.
    """
    try:
        if "andOver" in category:
            digits = "".join(filter(str.isdigit, category))
            return float(digits)
        else:
            parts = category.split("_")
            if len(parts) >= 2:
                low = float("".join(parts[:2]))
                high = float("".join(parts[2:])) if len(parts) > 2 else low
                return (low + high) / 2
    except Exception:
        return None

def get_salary_color(salary):
    """
    Détermine la couleur du marqueur en fonction du salaire médian.
    """
    min_sal, max_sal = 3000, 12000
    if salary is None:
        return "#808080"  # Gris si inconnu
    norm = (salary - min_sal) / (max_sal - min_sal)
    norm = max(0, min(1, norm))
    r = int(173 + norm * (255 - 173))
    g = int(216 + norm * (182 - 216))
    b = int(230 + norm * (193 - 230))
    return f"#{r:02x}{g:02x}{b:02x}"


def get_fill_color(price):
    """
    Retourne une couleur pour les polygones en fonction du prix de revente.
    L'échelle va de light yellow (#ffffcc) pour les faibles valeurs à dark red (#800026) pour les fortes valeurs.
    """
    min_price, max_price = 350_000, 900_000
    if price is None:
        return "#ffffff"
    
    norm = (price - min_price) / (max_price - min_price)
    norm = max(0, min(1, norm))  # Assurer que la valeur est entre 0 et 1

    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(rgb):
        return "#%02x%02x%02x" % rgb

    color1 = hex_to_rgb("#ffffcc")  # light yellow
    color2 = hex_to_rgb("#800026")  # dark red
    rgb = tuple(int(color1[i] + norm * (color2[i] - color1[i])) for i in range(3))
    
    return rgb_to_hex(rgb)

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


def create_folium_map_resale(geojson_path="services/data/processed/PriceWithSalaryUpdated.geojson"):
    """
    Crée une carte Folium affichant :
      - Les planning areas colorées selon le prix au mètre carré.
      - Des marqueurs positionnés sur le centroïde de chaque zone avec info sur le prix/m² et les revenus médians.
      - Une légende indiquant l'échelle des prix/m².
    """
    # Charger le GeoJSON
    with open(geojson_path, "r", encoding="utf-8") as f:
        geojson = json.load(f)

    # Créer la carte centrée sur Singapore
    m = folium.Map(location=[1.3521, 103.8198], zoom_start=11)

    # Style des polygones en fonction du prix/m²
    def style_function(feature):
        price = feature["properties"].get("resale_price")
        return {
            "fillColor": get_fill_color(price),
            "color": "black",
            "weight": 1,
            "fillOpacity": 0.7
        }

    folium.GeoJson(
        geojson,
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(fields=["PLN_AREA_N", "resale_price"], aliases=["Area:", "Resale price:"])
    ).add_to(m)


    # Ajout des cercles pour les salaires
    for feature in geojson["features"]:
        price = feature["properties"].get("resale_price")
        median_salary = feature["properties"].get("median_salary_category", "N/A")
        if price is None or price <= 0:
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
                <p>Working Population: {price}</p>
                <p>Median Salary: {salary_value if salary_value is not None else 'N/A'}</p>
            """, max_width=250)
        ).add_to(m)

    # Légende pour le resale_price
    price_legend = '''
     <div style="position: fixed; bottom: 50px; left: 50px; width: 180px; height: 140px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color: white; opacity: 0.8; padding: 10px;">
     <b>Resale price</b><br>
     350k - 500k: <i style="background:#ffffcc; width:20px; height:20px; display:inline-block"></i><br>
     500k - 650k: <i style="background:#fed976; width:20px; height:20px; display:inline-block"></i><br>
     650k - 800k: <i style="background:#fd8d3c; width:20px; height:20px; display:inline-block"></i><br>
     800k - 1000k: <i style="background:#800026; width:20px; height:20px; display:inline-block"></i>
     </div>
     '''
    m.get_root().html.add_child(folium.Element(price_legend))

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

# if __name__ == "__main__":
#     m = create_folium_map_resale()
#     m.save("folium_map_resale.html")


##########################################
# création de la figure de l'évolution des prix en fonction du quartier cliqué sur la map
##########################################

def create_line_chart_figure_history_price(town = "Ang Mo Kio"):
    """
    Crée une figure Plotly Express (line chart) pour l'évolution des prix.
    """
    df_agg = process_data_line_history()
    
    df_filtered = df_agg[df_agg["town"] == town]
    # data_list = df_filtered[["Date", "price_m2"]].to_dict(orient="records")

    # return dmc.LineChart(
    #     h=300,
    #     data=data,
    #     series=[{"name": "price_m2", "label": "Price per m2"}],
    #     dataKey="Date",
    #     type="gradient",
    #     strokeWidth=5,
    #     curveType="natural",
    #     yAxisProps={"domain": [4500.0, 7200.0]},  # Ajusté en fonction de la plage du prix
    #     p="lg",
    #     withLegend=True,
    #     tooltipAnimationDuration=200,
    #     unit=" SGD",
    # )

    fig = px.line(
        df_filtered,
        x="Date",
        y="price_m2",
        title="Price per m2 depending on the date",
    )
    return fig


def create_bar_chart_figure(selected_town="Ang Mo Kio"):
    df = process_data_line_history()

    # Filtrer les données pour 2024
    df_2024 = df[df["Year"] == 2024].groupby("town")["price_m2"].mean().reset_index()

    # Ajouter une colonne de couleur pour mettre en évidence le quartier sélectionné
    df_2024["color"] = df_2024["town"].apply(lambda x: "red" if x == selected_town else "lightgray")

    fig = px.bar(
        df_2024,
        x="town",
        y="price_m2",
        title="Prix moyen au m² en 2024",
        color="color",
        color_discrete_map="identity",  # Utilise les couleurs définies dans la colonne
    )

    fig.update_layout(
        xaxis_title="Quartier",
        yaxis_title="Prix au m²",
        template="plotly_white",
        xaxis_tickangle=-45  # Incline les noms des quartiers pour la lisibilité
    )

    return fig
