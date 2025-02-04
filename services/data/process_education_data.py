import pandas as pd

def create_bar_chart_data(detail_level="global", parent_value=None, year=2022, csv_path="services/data/raw/GraduateEmploymentSurvey.csv"):
    """
    Retourne les données formatées pour le BarChart de Dash Mantine Components en fonction du niveau de détail.

    Paramètres:
      - detail_level (str) : "global" pour une agrégation par université,
                              "university" pour une agrégation par école pour une université donnée,
                              "school" pour une agrégation par diplôme pour une école donnée.
      - parent_value (str) : Nom de l'université ou de l'école selon le niveau.
      - year (int) : Année d'analyse (par défaut 2022).
      - csv_path (str) : Chemin vers le fichier CSV.

    Retourne un dictionnaire contenant :
      - "data"    : Liste de dictionnaires (chaque dict représente une catégorie et sa valeur).
      - "dataKey" : La clé utilisée pour l’axe des x (ex. "university", "school" ou "degree").
      - "series"  : Liste d’objets définissant la mesure à afficher (ici le salaire médian) ;
                    nous n’y fixons pas de couleur pour que le BarChart applique sa palette par défaut.
    """
    df = pd.read_csv(csv_path)
    df["gross_monthly_median"] = pd.to_numeric(df["gross_monthly_median"], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df_year = df[df["year"] == year]
    
    if detail_level == "global":
        grouped = df_year.groupby("university", as_index=False)["gross_monthly_median"].median()
        grouped = grouped.sort_values(by="gross_monthly_median", ascending=False)
        data = []
        for _, row in grouped.iterrows():
            data.append({"university": row["university"], "gross_salary": row["gross_monthly_median"]})
        return {
            "data": data,
            "dataKey": "university",
            "series": [{"name": "gross_salary"}]  # pas de couleur fixée
        }
    elif detail_level == "university":
        if parent_value is None:
            raise ValueError("Veuillez fournir le nom de l'université dans parent_value pour le niveau 'university'.")
        df_uni = df_year[df_year["university"] == parent_value]
        grouped = df_uni.groupby("school", as_index=False)["gross_monthly_median"].median()
        grouped = grouped.sort_values(by="gross_monthly_median", ascending=False)
        data = []
        for _, row in grouped.iterrows():
            data.append({"school": row["school"], "gross_salary": row["gross_monthly_median"]})
        return {
            "data": data,
            "dataKey": "school",
            "series": [{"name": "gross_salary"}]
        }
    elif detail_level == "school":
        if parent_value is None:
            raise ValueError("Veuillez fournir le nom de l'école dans parent_value pour le niveau 'school'.")
        df_school = df_year[df_year["school"] == parent_value]
        grouped = df_school.groupby("degree", as_index=False)["gross_monthly_median"].median()
        grouped = grouped.sort_values(by="gross_monthly_median", ascending=False)
        data = []
        for _, row in grouped.iterrows():
            data.append({"degree": row["degree"], "gross_salary": row["gross_monthly_median"]})
        return {
            "data": data,
            "dataKey": "degree",
            "series": [{"name": "gross_salary"}]
        }
    else:
        raise ValueError("Niveau de détail non reconnu. Utilisez 'global', 'university' ou 'school'.")
