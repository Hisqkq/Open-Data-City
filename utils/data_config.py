import json
import pandas as pd

def load_data_config(json_path="assets/data_config.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config["datasets"]

def get_grouped_dataset_options():
    datasets = load_data_config()
    grouped = {}
    for d in datasets:
        group = d.get("group", "Other")
        if group not in grouped:
            grouped[group] = []
        grouped[group].append({"value": d["id"], "label": d["name"]})
    options = [{"group": group, "items": items} for group, items in grouped.items()]
    return options

def get_dataset_by_id(dataset_id):
    datasets = load_data_config()
    for d in datasets:
        if d["id"] == dataset_id:
            return d
    return None

def load_dataset(dataset_id):
    dataset = get_dataset_by_id(dataset_id)
    if dataset:
        return pd.read_csv(dataset["csv_path"])
    else:
        raise ValueError("Dataset not found")
