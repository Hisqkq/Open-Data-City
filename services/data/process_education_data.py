import pandas as pd
import numpy as np

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


import pandas as pd

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





if __name__ == "__main__":

    print(get_line_chart_data())
