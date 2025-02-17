import joblib
import pandas as pd

# Charger le modèle une seule fois au démarrage
MODEL_PATH = "models/catboost_model_entraine_compressed.pkl"
model = joblib.load(MODEL_PATH)

def predict_immobilier(data):
    """ Prédit le prix immobilier à partir des données fournies. """
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Input data must be a pandas DataFrame")
    
    # Faire la prédiction
    prediction = model.predict(data)
    
    return prediction