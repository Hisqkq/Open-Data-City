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





##########################################
# CREATION DE LA MAP SWITCH
##########################################



import folium
import json

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

def create_folium_map(geojson_path="services/data/processed/PriceWithSalary.geojson"):
    """
    Crée une carte Folium affichant :
      - Les planning areas colorées selon le prix au mètre carré.
      - Des marqueurs positionnés sur le centroïde de chaque zone avec info sur le prix/m².
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

    # Ajout des cercles pour afficher le prix/m² dans chaque quartier
    for feature in geojson["features"]:
        price = feature["properties"].get("price_m2")
        if price is None or price <= 0:
            continue
        centroid = feature["properties"].get("centroid")
        if not centroid:
            continue

        folium.CircleMarker(
            location=[centroid["lat"], centroid["lng"]],
            radius=7,  # Taille fixe pour bien voir les points
            color="black",
            fill=True,
            fill_color=get_fill_color(price),
            fill_opacity=0.9,
            popup=folium.Popup(f"""
                <h4>{feature["properties"].get("PLN_AREA_N", "")}</h4>
                <p>Price/m²: {price:.2f} SGD</p>
            """, max_width=250)
        ).add_to(m)

    # Légende pour le prix/m²
    price_legend = '''
     <div style="
     position: fixed; 
     bottom: 50px; left: 50px; width: 180px; height: 140px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color: white;
     opacity: 0.8;
     padding: 10px;
     ">
     <b>Price/m² Scale</b><br>
     3k - 5k: <i style="background:#ffffcc; width:20px; height:20px; display:inline-block"></i><br>
     5k - 7k: <i style="background:#fed976; width:20px; height:20px; display:inline-block"></i><br>
     7k - 9k: <i style="background:#fd8d3c; width:20px; height:20px; display:inline-block"></i><br>
     9k - 10k+: <i style="background:#800026; width:20px; height:20px; display:inline-block"></i>
     </div>
     '''
    m.get_root().html.add_child(folium.Element(price_legend))

    return m

if __name__ == "__main__":
    m = create_folium_map()
    m.save("folium_map_price.html")
