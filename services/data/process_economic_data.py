import pandas as pd

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


if __name__ == "__main__":
    preprocess_unemployment_data()
