import pandas as pd
import numpy as np
import warnings

## Get data functions for the education data

def get_aggregated_data(detail_level="global", parent_value=None, year=2022, csv_path="services/data/raw/GraduateEmploymentSurvey.csv"):
    """
    Retourne un DataFrame agrégé pour le graphique.
    
    Paramètres :
      - detail_level : "global" pour une agrégation par université,
                       "university" pour une agrégation par école pour une université donnée,
                       "school" pour une agrégation par diplôme pour une école donnée.
      - parent_value : valeur du niveau supérieur (nom d'université ou d'école) quand nécessaire.
      - year : année d'analyse.
      - csv_path : chemin vers le fichier CSV.
    
    Colonnes attendues dans le CSV :
      year, university, school, degree, employment_rate_overall, employment_rate_ft_perm,
      basic_monthly_mean, basic_monthly_median, gross_monthly_mean, gross_monthly_median,
      gross_mthly_25_percentile, gross_mthly_75_percentile
    """
    df = pd.read_csv(csv_path)
    
    # Conversion des colonnes numériques
    df["gross_monthly_median"] = pd.to_numeric(df["gross_monthly_median"], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    # Supprimer le "%" dans employment_rate_overall et convertir en nombre
    df["employment_rate_overall"] = pd.to_numeric(df["employment_rate_overall"].str.replace("%", ""), errors="coerce")
    
    df_year = df[df["year"] == year]
    
    if detail_level == "global":
        grouped = df_year.groupby("university", as_index=False).agg({
            "gross_monthly_median": "median",
            "employment_rate_overall": "mean"
        })
        grouped = grouped.sort_values(by="gross_monthly_median", ascending=False)
        return grouped
    elif detail_level == "university":
        if parent_value is None:
            raise ValueError("Veuillez fournir le nom de l'université pour le niveau 'university'.")
        df_uni = df_year[df_year["university"] == parent_value]
        grouped = df_uni.groupby("school", as_index=False).agg({
            "gross_monthly_median": "median",
            "employment_rate_overall": "mean"
        })
        grouped = grouped.sort_values(by="gross_monthly_median", ascending=False)
        return grouped
    elif detail_level == "school":
        if parent_value is None:
            raise ValueError("Veuillez fournir le nom de l'école pour le niveau 'school'.")
        df_school = df_year[df_year["school"] == parent_value]
        # Pour le niveau "school", on regroupe par "degree"
        grouped = df_school.groupby("degree", as_index=False).agg({
            "gross_monthly_median": "median",
            "employment_rate_overall": "mean"
        })
        # Ici, on trie par ordre alphabétique des diplômes pour une lecture plus claire.
        grouped = grouped.sort_values(by="degree", ascending=True)
        return grouped
    else:
        raise ValueError("Niveau de détail non reconnu. Utilisez 'global', 'university' ou 'school'.")


def get_line_chart_data(metric="intake_rate", gender="both", csv_path="services/data/processed/course_data.csv"):
    """
    Pré-traite et agrège les données pour créer un graphique linéaire.
    
    Paramètres:
      - metric : doit être l'une des valeurs suivantes : "intake", "enrolment", "graduates", "intake_rate"
      - gender : "both" (valeurs combinées, c'est-à-dire les colonnes avec suffixe _MF), "women" (suffixe _F), ou "men" (suffixe _men)
      - csv_path : chemin vers le fichier CSV prétraité.
      
    Retourne un DataFrame pivoté avec :
       - index : year
       - colonnes : courses
       - valeurs : moyenne (ou somme) de la métrique pour ce cours et cette année.
       
    Si le paramètre n'est pas valide, la fonction retourne un DataFrame vide.
    """
    # Liste des métriques autorisées et des genres autorisés
    allowed_metrics = {"intake", "enrolment", "graduates", "intake_rate"}
    allowed_genders = {"both", "women", "men"}
    
    if metric not in allowed_metrics:
        raise ValueError(f"Le paramètre 'metric' doit être l'une des valeurs suivantes : {allowed_metrics}")
    if gender not in allowed_genders:
        raise ValueError(f"Le paramètre 'gender' doit être l'une des valeurs suivantes : {allowed_genders}")
    
    # Charger le CSV
    df = pd.read_csv(csv_path)
        
    
    # Sélection de la colonne à utiliser
    if gender == "both":
        col_name = f"{metric}_MF" if metric != "intake_rate" else "intake_rate_MF"
    elif gender == "women":
        col_name = f"{metric}_F" if metric != "intake_rate" else "intake_rate_F"
    elif gender == "men":
        col_name = f"{metric}_men" if metric != "intake_rate" else "intake_rate_men"
    
    # Vérifier que la colonne existe dans le DataFrame
    if col_name not in df.columns:
        raise ValueError(f"La colonne '{col_name}' n'existe pas dans les données.")
    
    # Agrégation : pour chaque année et chaque cours, calcul de la moyenne de la colonne choisie.
    df_grouped = df.groupby(["year", "course"], as_index=False)[col_name].mean()
    
    # Pivot de la table pour obtenir une table avec index year, colonnes courses, et valeurs la métrique agrégée.
    df_pivot = df_grouped.pivot(index="year", columns="course", values=col_name)
    
    # Optionnel : trier les index (années) en ordre croissant
    df_pivot = df_pivot.sort_index()
    
    return df_pivot


def get_admission_trade_data(csv_path="services/data/processed/updated_annual_student_intake_enrolment.csv"):
    df = pd.read_csv(csv_path)
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["intake"] = pd.to_numeric(df["intake"], errors="coerce")
    df["enrolment"] = pd.to_numeric(df["enrolment"], errors="coerce")
    df["intake_rate"] = pd.to_numeric(df["intake_rate"], errors="coerce")

    return df

import pandas as pd

def get_institution_trends_data(metric="enrolment", institutions=None, csv_path="services/data/processed/institution_data.csv"):
    """
    Charge et agrège les données d'admission par institution sur plusieurs années.
    
    Paramètres:
      - metric : Indicateur à utiliser, parmi "enrolment", "intake" ou "intake_rate".
      - institutions : Liste des noms d'institutions à inclure. Si None, on prend toutes les institutions ayant une valeur non nulle pour la métrique.
      - csv_path : Chemin vers le fichier CSV contenant les colonnes :
            year, institution, enrolment, intake, intake_rate
       
    Retourne:
      Un DataFrame agrégé avec pour chaque (year, institution) la moyenne (ou valeur unique) de la métrique.
    """
    # Charger le CSV
    df = pd.read_csv(csv_path)
    
    # Conversion des colonnes numériques
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    for col in ["enrolment", "intake"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    # Pour intake_rate, si c'est déjà en pourcentage, on convertit en nombre (en gardant les décimales)
    df["intake_rate"] = pd.to_numeric(df["intake_rate"], errors="coerce")
    
    # Filtrer par institutions si une liste est fournie
    if institutions is not None and len(institutions) > 0:
        df = df[df["institution"].isin(institutions)]
    else:
        # On retire les lignes où la métrique est nulle pour éviter des traces vides
        df = df[df[metric].notnull()]
    
    # Agrégation : si pour une même institution et la même année plusieurs lignes existent,
    # on calcule la moyenne de la métrique.
    df_grouped = df.groupby(["year", "institution"], as_index=False)[metric].mean()
    df_grouped = df_grouped.sort_values(by="year")
    return df_grouped



## Preprocessing functions for the education data

def preprocess_course_data(csv_path="services/data/raw/IntakeEnrolmentGraduatesofUniversitiesbyCourse.csv"):
    """
    Charge et prétraite les données du CSV pour les cours.
    - Convertit les colonnes numériques.
    - Calcule la colonne intake_rate = 100 * intake / enrolment.
    - Réorganise les données pour disposer d'une ligne par (year, course) pour chaque genre :
        * Pour MF et F, on garde directement les valeurs.
        * Pour les hommes, on calcule : men = MF - F pour chaque métrique.
    
    Retourne un DataFrame avec les colonnes :
       year, course, 
       intake_MF, enrolment_MF, graduates_MF, intake_rate_MF,
       intake_F, enrolment_F, graduates_F, intake_rate_F,
       intake_men, enrolment_men, graduates_men, intake_rate_men
    """
    df = pd.read_csv(csv_path)
    
    # Conversion des colonnes numériques
    for col in ["intake", "enrolment", "graduates"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    
    # Calcul du taux d'admission pour chaque ligne (en %)
    df["intake_rate"] = np.where(df["enrolment"] > 0, 100 * df["intake"] / df["enrolment"], np.nan)
    
    # On pivote pour avoir MF et F sur une même ligne par (year, course)
    df_pivot = df.pivot_table(index=["year", "course"],
                              columns="sex",
                              values=["intake", "enrolment", "graduates", "intake_rate"],
                              aggfunc="first").reset_index()
    
    # Aplatir les colonnes multi-index
    df_pivot.columns = ["_".join(col).strip() if col[1] else col[0] for col in df_pivot.columns.values]
    
    # On attend que les colonnes soient nommées par exemple : year, course, intake_MF, intake_F, etc.
    # Calculer les valeurs pour les hommes en faisant la différence : hommes = MF - F
    for col in ["intake", "enrolment", "graduates"]:
        df_pivot[f"{col}_men"] = df_pivot.get(f"{col}_MF", np.nan) - df_pivot.get(f"{col}_F", np.nan)
    
    # Pour le taux d'admission des hommes, on calcule de façon similaire,
    # en évitant la division par zéro.
    df_pivot["intake_rate_men"] = np.where(
        (df_pivot.get("enrolment_MF", np.nan) - df_pivot.get("enrolment_F", np.nan)) > 0,
        100 * df_pivot.get("intake_MF", np.nan) - df_pivot.get("intake_F", np.nan) /
        (df_pivot.get("enrolment_MF", np.nan) - df_pivot.get("enrolment_F", np.nan)),
        np.nan
    )
    # Pour plus de sécurité, recalculons intake_rate_men de façon explicite :
    df_pivot["intake_rate_men"] = np.where(
        (df_pivot["enrolment_MF"] - df_pivot["enrolment_F"]) > 0,
        100 * df_pivot["intake_men"] / (df_pivot["enrolment_MF"] - df_pivot["enrolment_F"]),
        np.nan
    )

    # On save les donnes dans services/data/processed pour une utilisation future
    df_pivot.to_csv("services/data/processed/course_data.csv", index=False)
    # Remarque : selon vos données, il faudra peut-être ajuster la logique si certaines valeurs sont manquantes.
    return df_pivot


def calculate_annual_student_intake_and_enrolment(csv_path="services/data/raw/IntakeEnrolmentandGraduatesofUniversitiesbyCourse.csv", output_path="services/data/processed/annual_student_intake_enrolment.csv"):
    """
    Calcule par année le nombre d'étudiants qui s'inscrivent à l'université, en sommant sur la colonne intake et la colonne enrolment.
    Enregistre le résultat dans un nouveau fichier CSV.
    
    Paramètres:
        - csv_path : chemin vers le fichier CSV d'entrée.
        - output_path : chemin vers le fichier CSV de sortie.
    """
    df = pd.read_csv(csv_path)
    
    # Conversion des colonnes numériques
    df["intake"] = pd.to_numeric(df["intake"], errors="coerce")
    df["enrolment"] = pd.to_numeric(df["enrolment"], errors="coerce")

    # On filtre que sur la colonne sex = "MF" pour éviter les doublons
    df = df[df["sex"] == "MF"]

    # Agrégation par année
    df_aggregated = df.groupby("year").agg({
        "intake": "sum",
        "enrolment": "sum"
    }).reset_index()

    # On transforme les données en entiers pour éviter les décimales
    df_aggregated["intake"] = df_aggregated["intake"].astype(int)
    df_aggregated["enrolment"] = df_aggregated["enrolment"].astype(int)

    # On rajoute une colonne "intake rate" pour avoir le taux d'admission
    df_aggregated["intake_rate"] = 100 * df_aggregated["intake"] / df_aggregated["enrolment"]
    
    # Enregistrement du résultat dans un nouveau fichier CSV
    df_aggregated.to_csv(output_path, index=False)
    
    return df_aggregated

def transform_institution_data(enrolment_csv="services/data/raw/Enrolment by Institutions.csv", intake_csv="services/data/raw/Intake by Institutions.csv", output_csv="services/data/processed/institution_data.csv"):
    """
    Transforme les données d'enrolment et d'intake par institution pour obtenir un fichier CSV
    avec les colonnes: year, institution, enrolment, intake et intake_rate.
    
    Les fichiers d'entrée sont supposés avoir le format suivant:
      - Colonnes: year, sex, puis une série de colonnes pour les différentes institutions.
      - Chaque fichier comporte deux lignes par année (par exemple, une pour MF et une pour F).
    
    Le taux d'admission (intake_rate) est calculé en pourcentage: 100 * intake / enrolment.
    
    Parameters:
      - enrolment_csv (str) : chemin vers le fichier CSV "enrolment by institution".
      - intake_csv (str) : chemin vers le fichier CSV "intake by institution".
      - output_csv (str) : chemin où enregistrer le fichier transformé.
      
    Retourne:
      - df_merged (DataFrame): le DataFrame final.
    """
    # Charger le fichier d'enrolment
    df_enrolment = pd.read_csv(enrolment_csv)
    # On passe du format large au format long : identifier les colonnes institutionnelles.
    df_enrolment_long = df_enrolment.melt(id_vars=["year", "sex"], var_name="institution", value_name="enrolment")
    # S'assurer que la colonne 'enrolment' est numérique
    df_enrolment_long["enrolment"] = pd.to_numeric(df_enrolment_long["enrolment"], errors="coerce")
    # Agréger par year et institution en prennant la valeur maximale qui est toujours MF (pour avoir les données mixtes)
    df_enrolment_agg = df_enrolment_long.groupby(["year", "institution"], as_index=False)["enrolment"].max()
    
    # Charger le fichier d'intake
    df_intake = pd.read_csv(intake_csv)
    df_intake_long = df_intake.melt(id_vars=["year", "sex"], var_name="institution", value_name="intake")
    df_intake_long["intake"] = pd.to_numeric(df_intake_long["intake"], errors="coerce")
    df_intake_agg = df_intake_long.groupby(["year", "institution"], as_index=False)["intake"].max()
    
    # Fusionner les deux DataFrames sur year et institution
    df_merged = pd.merge(df_enrolment_agg, df_intake_agg, on=["year", "institution"], how="outer")
    
    # Calculer le taux d'admission (intake_rate) en pourcentage
    # On vérifie que l'enrolment n'est pas zéro pour éviter une division par zéro.
    df_merged["intake_rate"] = df_merged.apply(
        lambda row: 100 * row["intake"] / row["enrolment"] if pd.notnull(row["enrolment"]) and row["enrolment"] != 0 else None,
        axis=1
    )
    
    # Enregistrer le résultat dans un fichier CSV
    df_merged.to_csv(output_csv, index=False)
    return df_merged


def compute_corr_institution():
    """
    Calcule la corrélation entre les taux d'admission (intake_rate) et les effectifs (enrolment) par institution.
    """
    warnings.simplefilter(action="ignore", category=FutureWarning)

    df_intake = pd.read_csv("services/data/raw/Intake by Institutions.csv")
    df_enrolment = pd.read_csv("services/data/raw/Enrolment by Institutions.csv")

    # On filtre la colonne sex = "MF" et on drop la colonne sex
    df_intake = df_intake[df_intake["sex"] == "MF"].drop(columns=["sex"])
    df_enrolment = df_enrolment[df_enrolment["sex"] == "MF"].drop(columns=["sex"])

    df_intake_rate = df_intake.copy()

    # On calcule le taux d'admission
    df_intake_rate.iloc[:, 2:] = 100 * df_intake_rate.iloc[:, 2:] / df_enrolment.iloc[:, 2:]

    # On fait deux matrice des correlations en ommetant la colonne year dans les dataframes

    corr_intake = df_intake.drop(columns=["year"]).corr()
    corr_enrolment = df_enrolment.drop(columns=["year"]).corr()
    corr_intake_rate = df_intake_rate.drop(columns=["year"]).corr()

    return corr_intake, corr_enrolment, corr_intake_rate



if __name__ == "__main__":
    calculate_annual_student_intake_and_enrolment()
    transform_institution_data()
