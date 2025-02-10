import pandas as pd
import branca
import json
import re
import os

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
    # Identifier les colonnes des revenus (en supposant qu'elles commencent après "Planning Area")
    #on enlève la colonne 'Total'
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


    # Appliquer le mapping
    df_cum["median_income"] = df_cum["income_group"].map(income_median_mapping)

    return df_cum

def get_income_mapping():
    df_cum = process_data_map_income()  # Appelle ta fonction qui prépare les données
    return dict(zip(df_cum["Planning Area"], df_cum["median_income"]))


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
#     process_planning_area()