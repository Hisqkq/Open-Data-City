import json
import re
import os
from shapely.geometry import shape, mapping

def process_planning_area():
    # 📌 Chemins des fichiers
    RAW_GEOJSON_PATH = "services/data/raw/PlanningArea.geojson"
    PROCESSED_GEOJSON_PATH = "services/data/processed/PlanningArea.geojson"

    # 📌 Fonction pour extraire le nom des Planning Areas
    def extract_planning_area(description):
        match = re.search(r"<th>PLN_AREA_N<\/th> <td>(.*?)<\/td>", description)
        if match:
            name = match.group(1)
            return " ".join(word.capitalize() for word in name.split())  # 🔥 Majuscule sur chaque mot
        return "Unknown"

    # 📌 Charger le GeoJSON brut
    with open(RAW_GEOJSON_PATH, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    # 📌 Nettoyer et simplifier les données
    for feature in raw_data["features"]:
        description = feature["properties"].get("Description", "")
        feature["properties"]["PLN_AREA_N"] = extract_planning_area(description)

    # 📌 Sauvegarder le GeoJSON optimisé
    os.makedirs(os.path.dirname(PROCESSED_GEOJSON_PATH), exist_ok=True)
    with open(PROCESSED_GEOJSON_PATH, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, indent=4)

    print(f"✅ Fichier simplifié et sauvegardé dans {PROCESSED_GEOJSON_PATH}")



if __name__ == "__main__":
    process_planning_area()