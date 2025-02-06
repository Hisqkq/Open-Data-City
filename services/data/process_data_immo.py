import pandas as pd

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
