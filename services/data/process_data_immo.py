import pandas as pd
import branca
import json
import re
import os
from shapely.geometry import shape


# from process_economic_data import prepare_planning_areas_geojson

def process_data_immo():
    #chemin des fichiers
    RAW_DATA_PATH = "services/data/raw/immo.csv"

    #charger le fichier
    df = pd.read_csv(RAW_DATA_PATH)

    df["price_m2"] = df["resale_price"] / df["floor_area_sqm"]

    # Convertir 'Month' en datetime et extraire l'année
    df['month'] = pd.to_datetime(df['month'])
    df['Year'] = df['month'].dt.year
    df['Month'] = df['month'].dt.month

    df_grouped = df.groupby(["Year", "Month"])["price_m2"].mean().reset_index()
    df_grouped['Date'] = pd.to_datetime(df_grouped[['Year', 'Month']].assign(Day=1))

    return df_grouped

    # # Sauvegarder le fichier
    # PROCESSED_DATA_PATH = "services/data/processed/immo.csv"

    # df_grouped.to_csv(PROCESSED_DATA_PATH, index=False)

    # print(f"✅ Fichier traité et sauvegardé dans {PROCESSED_DATA_PATH}")

# if __name__ == "__main__":
#     process_data_immo()


def process_data_table_intro():
    #chemin des fichiers
    RAW_DATA_PATH = "services/data/raw/immo.csv"

    #charger le fichier
    df = pd.read_csv(RAW_DATA_PATH)

    # Convertir 'Month' en datetime et extraire l'année
    df['month'] = pd.to_datetime(df['month'])
    df['Year'] = df['month'].dt.year

    scd_grap_data = df[df["resale_price"] > 1000000]
    df_scd_graph = scd_grap_data.groupby("Year").size().reset_index(name="count")

    return df_scd_graph

def process_data_map_income():
    df_income = pd.read_csv("services/data/raw/income.csv")
    df_income = df_income.drop(columns=['Total'])
    income_cols = df_income.columns[1:]  # Supposons que la première colonne est 'Planning Area'

    # Appliquer la somme cumulative sur chaque ligne
    df_cum = df_income.copy()
    df_cum[income_cols] = df_income[income_cols].cumsum(axis=1) 

    df_cum['median_pop'] = df_cum['12_000andOver'] / 2

    ligne = df_cum.iloc[1].drop("Thousands")  # Supposons que 'Thousands' soit du texte

    for i in range(len(df_cum)):
        ligne = df_cum.iloc[i].drop("Thousands")
        for colonne, valeur in ligne.items():
            if valeur > ligne['median_pop']:
                df_cum.loc[i, 'income_group'] = colonne
                break

    # Dictionnaire pour mapper les tranches à leurs médianes
    income_median_mapping = {
        "Below_1_000": 500,
        "1_000_1_499": 1250,
        "1_500_1_999": 1750,
        "2_000_2_499": 2250,
        "2_500_2_999": 2750,
        "3_000_3_999": 3500,
        "4_000_4_999": 4500,
        "5_000_5_999": 5500,
        "6_000_6_999": 6500,
        "7_000_7_999": 7500,
        "8_000_8_999": 8500,
        "9_000_9_999": 9500,
        "10_000_10_999": 10500,
        "11_000_11_999": 11500,
        "12_000andOver": 12500
    }
    # on remplace le nom de la colonne 'Thousands' par 'PLN_AREA_N'
    df_cum = df_cum.rename(columns={'Thousands': 'PLN_AREA_N'})

    # Appliquer le mapping
    df_cum["median_income"] = df_cum["income_group"].map(income_median_mapping)

    return df_cum

def get_income_mapping():
    df_cum = process_data_map_income()

    # Renommer la colonne si nécessaire (vérifie bien son nom exact)
    if "Planning Area" in df_cum.columns:
        df_cum = df_cum.rename(columns={"Planning Area": "PLN_AREA_N"})

    return dict(zip(df_cum["PLN_AREA_N"], df_cum["median_income"]))  # Associe les quartiers aux revenus


def get_color_scale():
    return branca.colormap.linear.YlOrRd_09.scale(500, 12500)  # De 500€ à 12 500€


# Charger les données GeoJSON
def process_planning_area():
    # 📌 Chemins des fichiers
    RAW_GEOJSON_PATH = "services/data/raw/areazone.geojson"
    PROCESSED_GEOJSON_PATH = "services/data/processed/areazone.geojson"

    # 📌 Fonction pour extraire le nom des Planning Areas
    def extract_planning_area(description):
        match = re.search(r"<th>PLN_AREA_N<\/th> <td>(.*?)<\/td>", description)
        if match:
            name = match.group(1)
            return " ".join(word.capitalize() for word in name.split())  # 🔥 Majuscule sur chaque mot
        return "Unknown"

    # 📌 Charger le GeoJSON brut
    with open(RAW_GEOJSON_PATH, "r", encoding="utf-8") as f:
        areazone_data = json.load(f)

    # 📌 Nettoyer et simplifier les données
    for feature in areazone_data["features"]:
        description = feature["properties"].get("Description", "")
        feature["properties"]["PLN_AREA_N"] = extract_planning_area(description)

    # 📌 Sauvegarder le GeoJSON optimisé
    os.makedirs(os.path.dirname(PROCESSED_GEOJSON_PATH), exist_ok=True)
    with open(PROCESSED_GEOJSON_PATH, "w", encoding="utf-8") as f:
        json.dump(areazone_data, f, indent=4)

    print(f"✅ Fichier simplifié et sauvegardé dans {PROCESSED_GEOJSON_PATH}")

# if __name__ == "__main__":
#     geojson_data = prepare_planning_areas_geojson(background_variable= "price_m2")

#     # Écriture dans un fichier GeoJSON
#     with open("services/data/processed/PriceWithSalary.geojson", "w", encoding="utf-8") as f:
#         json.dump(geojson_data, f, ensure_ascii=False, indent=4)


#####################
# PROCESS POUR DONNEES CARTE SWITCH
#####################



#####################
# PROCESS POUR DONNEES CARTE SWITCH
#####################

def prepare_planning_areas_geojson(geojson_path="services/data/processed/PlanningArea.geojson",
                                   output_path="services/data/processed/PriceWithSalary.geojson"):
    """
    Charge le GeoJSON des planning areas et les CSV contenant :
      - price_m2 : le prix moyen du m² pour l'année 2017
      - resale_price : le prix moyen de revente d'un logement en 2017
    Enrichit chaque feature du GeoJSON avec ces valeurs.
    """

    # Charger le CSV des prix au m²
    df_price = pd.read_csv("services/data/processed/immo_map_price.csv")
    df_price = df_price[df_price["Year"] == 2017]  # Filtrer pour l'année 2017
    df_price["town"] = df_price["town"].str.strip().str.upper()  # Normaliser les noms

    # Charger le CSV des prix de revente
    df_resale = pd.read_csv("services/data/processed/df_grouped_resale.csv")
    df_resale = df_resale[df_resale["Year"] == 2017]  # Filtrer pour l'année 2017
    df_resale["town"] = df_resale["town"].str.strip().str.upper()  # Normaliser les noms

    # Charger le GeoJSON
    with open(geojson_path, "r", encoding="utf-8") as f:
        geojson = json.load(f)

    # Mettre à jour les propriétés des features selon la planning area
    for feature in geojson["features"]:
        area_name = feature["properties"].get("PLN_AREA_N", "").strip().upper()

        # Ajouter price_m2
        row_price = df_price[df_price["town"] == area_name]
        if not row_price.empty:
            feature["properties"]["price_m2"] = float(row_price.iloc[0]["price_m2"])

        # Ajouter resale_price
        row_resale = df_resale[df_resale["town"] == area_name]
        if not row_resale.empty:
            feature["properties"]["resale_price"] = float(row_resale.iloc[0]["resale_price"])

    # Ajouter le centroïde pour chaque zone si non présent
    for feature in geojson["features"]:
        if "centroid" not in feature["properties"]:
            geom = feature["geometry"]
            poly = shape(geom)
            centroid = poly.centroid
            feature["properties"]["centroid"] = {"lat": centroid.y, "lng": centroid.x}

    # Sauvegarder le GeoJSON enrichi
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(geojson, f, indent=4)

    return geojson

def merge_salary_data(price_geojson_path="services/data/processed/PriceWithSalary.geojson",
                      salary_geojson_path="services/data/processed/PlanningAreaWithSalary.geojson",
                      output_path="services/data/processed/PriceWithSalaryUpdated.geojson"):
    """
    Fusionne les données de salaire (working_population, median_salary_category) depuis 
    PlanningAreaWithSalary.geojson dans PriceWithSalary.geojson en faisant correspondre les zones de planification (PLN_AREA_N).
    """
    
    # Charger le GeoJSON des salaires
    with open(salary_geojson_path, "r", encoding="utf-8") as f:
        salary_geojson = json.load(f)

    # Construire un dictionnaire pour un accès rapide aux données de salaire
    salary_data = {}
    for feature in salary_geojson["features"]:
        area_name = feature["properties"].get("PLN_AREA_N", "").strip().upper()
        salary_data[area_name] = {
            "working_population": feature["properties"].get("working_population"),
            "median_salary_category": feature["properties"].get("median_salary_category"),
        }

    # Charger le GeoJSON des prix
    with open(price_geojson_path, "r", encoding="utf-8") as f:
        price_geojson = json.load(f)

    # Mettre à jour les propriétés des features du GeoJSON des prix
    for feature in price_geojson["features"]:
        area_name = feature["properties"].get("PLN_AREA_N", "").strip().upper()
        
        # Vérifier si on a les données de salaire correspondantes
        if area_name in salary_data:
            feature["properties"]["working_population"] = salary_data[area_name]["working_population"]
            feature["properties"]["median_salary_category"] = salary_data[area_name]["median_salary_category"]

    # Sauvegarder le GeoJSON mis à jour
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(price_geojson, f, indent=4)

    return price_geojson

# if __name__ == "__main__":
#     merge_salary_data()


# if __name__ == "__main__":
#     prepare_planning_areas_geojson()