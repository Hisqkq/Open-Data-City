import pandas as pd
import numpy as np
import json
from shapely.geometry import shape


def get_unemployment_by_city(csv_path="services/data/raw/UnemploymentRate.csv"):
    """
    Récupère le taux de chômage par ville.
    """
    df = pd.read_csv(csv_path)
    return df

def get_overall_unemployment_rate(csv_path="services/data/raw/OverallUnemploymentRateAnnual.csv"):
    """
    Récupère et formate le taux de chômage de Singapour au fil des ans.
    """
    df = pd.read_csv(csv_path)
    df = df[df["residential_status"] == "overall"]  # Filtrer pour ne garder que les valeurs globales
    df = df[["year", "unemployment_rate"]].dropna()  # Garder uniquement les colonnes nécessaires
    df["year"] = df["year"].astype(str)  # Convertir l'année en chaîne pour l'affichage
    return df.to_dict(orient="records")  # Retourner sous forme de liste de dictionnaires



def get_unemployment_by_age(csv_path="services/data/raw/unemployment_by_age.csv"):
    """
    Lit le CSV contenant les données de chômage par tranche d'âge et les pivotte, pour les résidents de Singapour.
    Attendu :
      - Colonnes: year, age, unemployment_rate
    Retourne une liste de dictionnaires avec pour chaque année, une clé pour chaque tranche d'âge.
    """
    df = pd.read_csv(csv_path)
    # Pivot : chaque ligne correspond à une année, et les colonnes aux tranches d'âge.
    pivot = df.pivot(index="year", columns="age", values="unemployment_rate").reset_index()
    return pivot.to_dict(orient="records")


def get_unemployment_by_qualification(csv_path="services/data/raw/unemployment_by_qualification.csv"):
    """
    Lit le CSV contenant les données de chômage par niveau de qualification et les pivotte, pour les résidents de Singapour.
    Attendu :
      - Colonnes: year, highest_qualification_attained, unemployment_rate
    Retourne une liste de dictionnaires avec pour chaque année, une clé pour chaque niveau de qualification.
    """
    df = pd.read_csv(csv_path)
    pivot = df.pivot(index="year", columns="highest_qualification_attained", values="unemployment_rate").reset_index()
    return pivot.to_dict(orient="records")


def get_unemployment_by_sex(csv_path="services/data/raw/unemployment_by_sex.csv"):
    """
    Lit le CSV contenant les données de chômage par sexe et les pivotte, pour les résidents de Singapour.
    Attendu :
      - Colonnes: year, sex, unemployment_rate
    Retourne une liste de dictionnaires avec pour chaque année, des colonnes 'Male' et 'Female'.
    """
    df = pd.read_csv(csv_path)
    pivot = df.pivot(index="year", columns="sex", values="unemployment_rate").reset_index()
    pivot = pivot.rename(columns={"male": "Male", "female": "Female"})
    return pivot.to_dict(orient="records")





def preprocess_unemployment_data(csv_path="services/data/raw/ResidentLabourForceAged15YearsandOverbyLabourForceStatusAgeAndSex.csv"):
    """
    Prétraite les données de chômage et calcule les taux de chômage globaux,
    par sexe et par tranche d'âge.

    Paramètres :
        csv_path (str) : Chemin vers le fichier CSV contenant les données.

    Retourne :
        df (DataFrame) : DataFrame contenant les taux de chômage globaux, par sexe et par tranche d'âge.
    """
    df = pd.read_csv(csv_path)

    # Calcul du taux de chômage global par année
    df_overall = df.groupby("year").agg(
        total_unemployed=("unemployed", "sum"),
        total_labour_force=("labour_force", "sum")
    )
    df_overall["unemployment_rate_overall"] = df_overall["total_unemployed"] / df_overall["total_labour_force"] * 100

    # Calcul du taux de chômage par sexe
    df_sex = df.groupby(["year", "sex"]).agg(
        total_unemployed=("unemployed", "sum"),
        total_labour_force=("labour_force", "sum")
    ).reset_index()

    df_sex["unemployment_rate"] = df_sex["total_unemployed"] / df_sex["total_labour_force"] * 100
    df_sex_pivot = df_sex.pivot(index="year", columns="sex", values="unemployment_rate")
    df_sex_pivot.columns = [f"unemployment_rate_{col}" for col in df_sex_pivot.columns]

    # Calcul du taux de chômage par tranche d'âge
    df_age = df.groupby(["year", "sex", "age"]).agg(
        total_unemployed=("unemployed", "sum"),
        total_labour_force=("labour_force", "sum")
    ).reset_index()

    df_age["unemployment_rate"] = df_age["total_unemployed"] / df_age["total_labour_force"] * 100
    df_age_pivot = df_age.pivot(index=["year", "age"], columns="sex", values="unemployment_rate")
    df_age_pivot.columns = [f"unemployment_rate_{col}" for col in df_age_pivot.columns]
    df_age_pivot = df_age_pivot.reset_index()

    # Fusionner les résultats
    df_final = df_overall.reset_index().merge(df_sex_pivot, on="year").merge(df_age_pivot, on="year", how="left")

    # save the processed data to a new CSV file
    df_final.to_csv("services/data/processed/UnemploymentRateProcessed.csv", index=False)

    return df_final


def preprocess_salary_data(csv_path="services/data/raw/ResidentWorkingPersonsAged15YearsandOverbyPlanningAreaandGrossMonthlyIncomefromWorkGeneralHouseholdSurvey2015.csv"):
    """
    Prétraite les données de population par planning area afin de calculer :
      - working_population : la somme des travailleurs sur toutes les tranches de salaire,
      - median_salary_category : la catégorie dans laquelle se situe le salaire médian.
      
    Le CSV est supposé avoir la structure suivante :
      Thousands,Total,Below_1_000,1_000_1_499,1_500_1_999,2_000_2_499,2_500_2_999,
      3_000_3_999,4_000_4_999,5_000_5_999,6_000_6_999,7_000_7_999,
      8_000_8_999,9_000_9_999,10_000_10_999,11_000_11_999,12_000andOver
      
    - La première colonne correspond au nom de la planning area (nous la renommons "PlanningArea").
    - La deuxième colonne ("Total") est ignorée dans le calcul.
    - Les colonnes de répartition (à partir de la 3e colonne) sont additionnées pour obtenir la population.
    - La catégorie médiane est déterminée en calculant la somme cumulative sur les colonnes de répartition
      et en renvoyant la première catégorie pour laquelle la somme cumulative atteint ou dépasse la moitié de la population totale.
    
    Retourne un DataFrame avec les colonnes :
      - PlanningArea
      - working_population
      - median_salary_category
    """
    # Charger le CSV
    df = pd.read_csv(csv_path)
    # Renommer la première colonne en "PlanningArea"
    df.rename(columns={df.columns[0]: "PlanningArea"}, inplace=True)
    
    # Les colonnes de répartition sont toutes les colonnes à partir de la 3e (index 2)
    breakdown_cols = df.columns[2:]
    
    # Calcul de la population totale en sommant les colonnes de répartition
    df["working_population"] = df[breakdown_cols].sum(axis=1)
    # On convertit la colonne en int pour éviter les problèmes de calcul
    
    # Fonction pour déterminer la catégorie médiane
    def find_median_category(row):
        total = row["working_population"]
        half = total / 2
        cum_sum = 0
        for col in breakdown_cols:
            cum_sum += row[col]
            if cum_sum >= half:
                return col  # Retourne le nom de la colonne correspondante à la médiane
        return None
    
    df["median_salary_category"] = df.apply(find_median_category, axis=1)

    df["working_population"] = df["working_population"] * 1000
    df["working_population"] = df["working_population"].astype(int)
   
    # Retourner uniquement les colonnes utiles
    return df[["PlanningArea", "working_population", "median_salary_category"]]

def prepare_planning_areas_geojson(geojson_path="services/data/processed/PlanningArea.geojson",
                                   csv_path="services/data/raw/ResidentWorkingPersonsAged15YearsandOverbyPlanningAreaandGrossMonthlyIncomefromWorkGeneralHouseholdSurvey2015.csv",
                                   output_path="services/data/processed/PlanningAreaWithSalary.geojson",
                                   background_variable="working_population"):
    """
    Charge le GeoJSON des planning areas et le CSV de données (population et median salary category),
    puis enrichit chaque feature du GeoJSON en ajoutant :
      - population: la population des travailleurs (en milliers)
      - median_salary: la valeur de la catégorie de salaire médian
    Le CSV est supposé avoir la structure suivante (avec une ligne "Total" à ignorer) :
      PlanningArea,Total,Below_1_000,1_000_1_499,...,12_000andOver
    On utilisera la colonne "Total" pour la population et la dernière colonne pour la catégorie de salaire.
    """
    # Charger le CSV et ignorer la ligne "Total"
    df = preprocess_salary_data(csv_path)
    
    # Supposons que la première colonne est le nom de la planning area, la deuxième la population,
    # et la dernière colonne la valeur correspondant à la catégorie de salaire médian.
    df["PlanningArea"] = df.iloc[:,0].str.strip()
    df[background_variable] = pd.to_numeric(df.iloc[:,1], errors="coerce")
    
    # Charger le GeoJSON
    with open(geojson_path, "r", encoding="utf-8") as f:
        geojson = json.load(f)
    
    # Mettre à jour les propriétés des features selon le planning area
    for feature in geojson["features"]:
        # On suppose que le nom de la planning area est dans la propriété "PLN_AREA_N"
        area_name = feature["properties"].get("PLN_AREA_N", "").strip()
        # Rechercher la ligne correspondante (en comparant en majuscules)
        row = df[df["PlanningArea"].str.upper() == area_name.upper()]
        if not row.empty:
            feature["properties"][background_variable] = int(row.iloc[0][background_variable])
            feature["properties"]["median_salary_category"] = row.iloc[0]["median_salary_category"]

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



if __name__ == "__main__":
    prepare_planning_areas_geojson()
