### QUANTILE REGRESSION MODEL FOR INTAKE ENROLMENT PREDICTION ###

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from scipy.stats import boxcox

def intake_enrolment_pred():

    df = pd.read_csv("services/data/processed/annual_student_intake_enrolment.csv")

    # Appliquer la transformation Box-Cox
    df["intake_boxcox"], lambda_intake = boxcox(df["intake"])
    df["enrolment_boxcox"], lambda_enrolment = boxcox(df["enrolment"])

    print(f"Meilleur lambda pour Box-Cox (intake): {lambda_intake}")
    print(f"Meilleur lambda pour Box-Cox (enrolment): {lambda_enrolment}")

    # Entraînement des modèles quantile (q=0.5)
    model_qr_intake = smf.quantreg('intake_boxcox ~ year', df).fit(q=0.5)
    model_qr_enrolment = smf.quantreg('enrolment_boxcox ~ year', df).fit(q=0.5)

    # Prédiction sur les années existantes
    df["intake_pred_boxcox"] = model_qr_intake.predict(df)
    df["enrolment_pred_boxcox"] = model_qr_enrolment.predict(df)

    # Fonction pour inverser la transformation Box-Cox
    def inverse_boxcox(y, lambda_):
        return np.exp(np.log(lambda_ * y + 1) / lambda_) if lambda_ != 0 else np.exp(y)

    # Appliquer l'inversion sur les prédictions
    df["intake_pred"] = inverse_boxcox(df["intake_pred_boxcox"], lambda_intake)
    df["enrolment_pred"] = inverse_boxcox(df["enrolment_pred_boxcox"], lambda_enrolment)

    # Calcul de intake_rate_pred
    df["intake_rate_pred"] = (df["intake_pred"] / df["enrolment_pred"]) * 100

    # Ajouter les nouvelles années (2024-2028)
    future_years = pd.DataFrame({"year": np.arange(2024, 2029)})
    future_years["intake_pred_boxcox"] = model_qr_intake.predict(future_years)
    future_years["enrolment_pred_boxcox"] = model_qr_enrolment.predict(future_years)

    # Appliquer l'inversion sur les nouvelles années
    future_years["intake_pred"] = inverse_boxcox(future_years["intake_pred_boxcox"], lambda_intake)
    future_years["enrolment_pred"] = inverse_boxcox(future_years["enrolment_pred_boxcox"], lambda_enrolment)

    # Calcul de intake_rate_pred pour les nouvelles années
    future_years["intake_rate_pred"] = (future_years["intake_pred"] / future_years["enrolment_pred"]) * 100

    # Fusionner avec les données existantes
    df = pd.concat([df, future_years], ignore_index=True)

    # Sauvegarde des données mises à jour
    df.to_csv("services/data/processed/updated_annual_student_intake_enrolment.csv", index=False)

    return df, model_qr_intake, model_qr_enrolment

if __name__ == "__main__":
    df, model_qr_intake, model_qr_enrolment = intake_enrolment_pred()

    # Modèle intake
    print(model_qr_intake.summary())

    # Modèle enrolment
    print(model_qr_enrolment.summary())
