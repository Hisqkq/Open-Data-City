import pandas as pd
import numpy as np
import json
import scipy.stats
from shapely.geometry import shape
from scipy.linalg import inv
from itertools import combinations


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

def get_combined_cpi_salary_data(cpi_csv="services/data/processed/CPI_transformed.csv",
                                 salary_csv="services/data/processed/median_income_transformed.csv",
                                 cpi_columns=None):
    """
    Combine les données du Consumer Price Index (CPI) et de l'évolution du salaire médian.
    
    Paramètres :
      - cpi_csv : chemin vers le CSV transformé du CPI.
      - salary_csv : chemin vers le CSV transformé du salaire médian (contenant la colonne "index").
      - cpi_columns : liste des colonnes du CPI à conserver (si None, on conserve toutes sauf "year_month").
    
    Retourne :
      - Une liste de dictionnaires (via .to_dict("records")) avec une colonne "year_month" 
        et pour chaque catégorie du CPI ainsi que la colonne "Median Salary Index" (l'ancienne "index").
    """
    # Charger les données CPI
    df_cpi = pd.read_csv(cpi_csv)
    df_salary = pd.read_csv(salary_csv)[["year_month", "index"]]    
    df_cpi = pd.merge(df_cpi, df_salary, on="year_month", how="inner")
    # on renomme la colonne index en Median Salary Index
    df_cpi.rename(columns={"index": "Median Salary Index"}, inplace=True)

    if cpi_columns is None:
        cpi_columns = [col for col in df_cpi.columns if col != "year_month"]
    df_cpi = df_cpi[["year_month"] + cpi_columns]
    
    # Renommer la colonne "index" en "Median Salary Index" pour plus de clarté
    if "index" in df_cpi.columns:
        df_cpi.rename(columns={"index": "Median Salary Index"}, inplace=True)
    
    return df_cpi.to_dict("records")

def get_cpi_multiselect(cpi_csv="services/data/processed/CPI_transformed.csv", salary_csv="services/data/processed/median_income_transformed.csv"):
    """
    Retourne une liste d'options pour le multiselect du graphique CPI.
    
    Cette fonction lit le CSV transformé du CPI et retourne une liste de dictionnaires 
    de la forme [{"value": <colonne>, "label": <colonne>}, ...] pour toutes les colonnes 
    (catégories CPI) à l'exception de "year_month".
    
    Paramètres :
      - cpi_csv : chemin vers le fichier CSV transformé du CPI.
      - salary_csv : (non utilisé ici, mais conservé pour compatibilité)
    
    Retourne :
      - options : liste d'options pour un composant dmc.Select ou dmc.MultiSelect.
    """
    # Lire le fichier CSV transformé
    df_cpi = pd.read_csv(cpi_csv)
    
    # Nettoyer les noms de colonnes (supprimer les espaces superflus)
    df_cpi.columns = df_cpi.columns.str.strip()
    
    # Exclure la colonne "year_month" qui sert d'index temporel
    cpi_columns = [col for col in df_cpi.columns if col != "year_month"]
    
    # Créer la liste des options pour le multiselect
    options = [{"value": col, "label": col} for col in cpi_columns]
    # On ajoute l'option "Index salaire médian" pour comparer avec le CPI
    options.append({"value": "Median Salary Index", "label": "Median Salary Index"})

    values = ["All Items", "Food", "Clothing & Footwear", "Housing & Utilities", "Household Durables & Services", "Health Care", "Transport", "Communication", "Recreation & Culture", "Education", "Personal Care", "Alcoholic Drinks & Tobacco", "Public Transport", "Median Salary Index"]

    return options, values

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
    df.rename(columns={df.columns[0]: "PlanningArea"}, inplace=True)
    
    breakdown_cols = df.columns[2:]
    
    df["working_population"] = df[breakdown_cols].sum(axis=1)
    
    def find_median_category(row):
        total = row["working_population"]
        half = total / 2
        cum_sum = 0
        for col in breakdown_cols:
            cum_sum += row[col]
            if cum_sum >= half:
                return col  
        return None
    
    df["median_salary_category"] = df.apply(find_median_category, axis=1)

    df["working_population"] = df["working_population"] * 1000
    df["working_population"] = df["working_population"].astype(int)
    
    # Retourner uniquement les colonnes utiles
    return df[["PlanningArea", "working_population", "median_salary_category"]]

def prepare_planning_areas_geojson(geojson_path="services/data/processed/PlanningArea.geojson",
                                   csv_path="services/data/raw/ResidentWorkingPersonsAged15YearsandOverbyPlanningAreaandGrossMonthlyIncomefromWorkGeneralHouseholdSurvey2015.csv",
                                   output_path="services/data/processed/PlanningAreaWithSalary.geojson"):
    """
    Charge le GeoJSON des planning areas et le CSV de données (population et median salary category),
    puis enrichit chaque feature du GeoJSON en ajoutant :
      - population: la population des travailleurs (en milliers)
      - median_salary: la valeur de la catégorie de salaire médian
    Le CSV est supposé avoir la structure suivante (avec une ligne "Total" à ignorer) :
      PlanningArea,Total,Below_1_000,1_000_1_499,...,12_000andOver
    On utilisera la colonne "Total" pour la population et la dernière colonne pour la catégorie de salaire.
    """
    df = preprocess_salary_data(csv_path)
    

    df["PlanningArea"] = df.iloc[:,0].str.strip()
    df["working_population"] = pd.to_numeric(df.iloc[:,1], errors="coerce")
    
    with open(geojson_path, "r", encoding="utf-8") as f:
        geojson = json.load(f)
    
    for feature in geojson["features"]:
        area_name = feature["properties"].get("PLN_AREA_N", "").strip()
        row = df[df["PlanningArea"].str.upper() == area_name.upper()]
        if not row.empty:
            feature["properties"]["working_population"] = int(row.iloc[0]["working_population"])
            feature["properties"]["median_salary_category"] = row.iloc[0]["median_salary_category"]

    for feature in geojson["features"]:
        if "centroid" not in feature["properties"]:
            geom = feature["geometry"]
            poly = shape(geom)
            centroid = poly.centroid
            feature["properties"]["centroid"] = {"lat": centroid.y, "lng": centroid.x}

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(geojson, f, indent=4)

    return geojson

def preprocess_CPI_data(csv_path="services/data/raw/ConsumerPriceIndexCPI2019AsBaseYearMonthly.csv"):
    # Lecture du fichier CSV d'origine
    df = pd.read_csv(csv_path)
    
    df["DataSeries"] = df["DataSeries"].str.strip()
    
    melted = pd.melt(df, id_vars=["DataSeries"], var_name="year_month", value_name="CPI")
    
    pivot_df = melted.pivot(index="year_month", columns="DataSeries", values="CPI").reset_index()

    # On garde les valeurs au dela de April 2000
    pivot_df = pivot_df[pivot_df["year_month"] >= "2000"]

    pivot_df["year_month"] = pivot_df["year_month"].apply(lambda x: x[:4] + "-" + x[4:])

    pivot_df = pivot_df[['year_month', 'All Items', 'Food', 'Clothing & Footwear', 'Housing & Utilities', 'Household Durables & Services', 'Health Care', 'Transport', 'Communication', 'Recreation & Culture', 'Education', 'Personal Care', 'Alcoholic Drinks & Tobacco', 'Public Transport']]
    
    pivot_df.to_csv("services/data/processed/CPI_transformed.csv", index=False)
    
    print("Transformation terminée. Le fichier 'CPI_transformed.csv' a été enregistré.")
    return pivot_df

def transform_med_income(csv_path="services/data/raw/MedianGrossMonthlyIncomeFromEmploymentofFullTimeEmployedResidentsTotal.csv", base_date="2019-06-01", output_csv="services/data/processed/median_income_transformed.csv"):
    """
    Transforme le CSV annuel de salaire médian en un DataFrame mensuel interpolé, avec les colonnes suivantes :
      - year         : année (numérique)
      - month        : mois (abrégé, par exemple "Jan", "Feb", …)
      - year_month   : chaîne de caractère "YYYY-MMM"
      - med_income_incl_empcpf : salaire médian interpolé pour le mois
      - index        : indice calculé par rapport à la valeur de référence (base_date)
    
    On considère que les valeurs annuelles correspondent au mois de juin de chaque année.
    La fonction enregistre le résultat dans output_csv et retourne le DataFrame.
    """
    # Lire le CSV
    df = pd.read_csv(csv_path)
    
    df = df[['year', 'med_income_incl_empcpf']]
    
    df['date'] = pd.to_datetime(df['year'].astype(str) + "-06-01")
    df = df.set_index('date')
    
    new_index = pd.date_range(start=df.index.min(), end=df.index.max(), freq='MS')  # "MS": début de mois
    
    df_monthly = df.reindex(new_index)
    df_monthly['med_income_incl_empcpf'] = df_monthly['med_income_incl_empcpf'].interpolate(method='linear')
    
    df_monthly = df_monthly.reset_index().rename(columns={'index': 'date'})
    
    df_monthly['year'] = df_monthly['date'].dt.year
    df_monthly['month'] = df_monthly['date'].dt.strftime('%b')
    df_monthly['year_month'] = df_monthly['date'].dt.strftime('%Y-%b')
    
    # Récupérer la valeur de référence pour l'indexation (base_date, ici juin 2019)
    base_value_series = df_monthly.loc[df_monthly['date'] == pd.to_datetime(base_date), 'med_income_incl_empcpf']
    if base_value_series.empty:
        raise ValueError(f"Base date {base_date} non trouvée dans les données.")
    base_value = base_value_series.iloc[0]
    
    df_monthly['index'] = df_monthly['med_income_incl_empcpf'] / base_value * 100
    
    df_monthly = df_monthly[['year', 'month', 'year_month', 'med_income_incl_empcpf', 'index']]
    
    df_monthly.to_csv(output_csv, index=False)
    
    return df_monthly


def compute_partial_correlation_matrix(alpha=0.05):
    """
    Calcule la matrice des corrélations partielles et la matrice d'adjacence après correction de Bonferroni.
    Retourne :
    - adj_matrix : matrice binaire des liens significatifs.
    - corr_matrix : matrice des corrélations partielles.
    - var_names : noms des variables (pour les nœuds du graphe).
    """
    df_cpi = pd.read_csv("services/data/processed/CPI_transformed.csv").drop(columns=["All Items"])
    df_salary = pd.read_csv("services/data/processed/median_income_transformed.csv")[["year_month", "index"]]
    df_salary.rename(columns={"index": "Median Salary Index"}, inplace=True)

    df = pd.merge(df_cpi, df_salary, on="year_month", how="inner").drop(columns=["year_month"])

    df_std = (df - df.mean()) / df.std()

    precision_matrix = inv(df_std.corr().values)  
    n_vars = df_std.shape[1]
    corr_partial = np.zeros((n_vars, n_vars))
    p_values = np.zeros((n_vars, n_vars))

    for i, j in combinations(range(n_vars), 2):
        theta_ij = precision_matrix[i, j]
        theta_ii = precision_matrix[i, i]
        theta_jj = precision_matrix[j, j]
        corr_partial[i, j] = -theta_ij / np.sqrt(theta_ii * theta_jj)
        corr_partial[j, i] = corr_partial[i, j]

        dof = df_std.shape[0] - n_vars
        z_score = 0.5 * np.log((1 + corr_partial[i, j]) / (1 - corr_partial[i, j])) * np.sqrt(dof)
        p_values[i, j] = 2 * (1 - scipy.stats.norm.cdf(np.abs(z_score)))
        p_values[j, i] = p_values[i, j]

    alpha_corr = alpha / (n_vars * (n_vars - 1) / 2)
    adj_matrix = (p_values < alpha_corr).astype(int)

    return adj_matrix, corr_partial, df.columns.tolist()



if __name__ == "__main__":
    prepare_planning_areas_geojson()
    preprocess_CPI_data()
    transform_med_income()
