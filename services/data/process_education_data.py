import pandas as pd

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
