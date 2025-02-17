GITHUB_LINK = "https://github.com/Hisqkq/Open-Data-City"  

NAV_LINKS = {
    "Home": ["/", "bi:house-door-fill"],
    "Topics": {
        "Housing": ["/housing", "icon-park-outline:building-one"],
        "Education": ["/education", "tabler:book"],
        "Economy": ["/economy", "tabler:currency-dollar"]
    },
    "Other": {
        "Data": ["/data", "tabler:gauge"],
        "About Us": ["/about-us", "tabler:user"]
    }
}

TOWNS = [
            {"label": "Ang Mo Kio", "value": "Ang Mo Kio"},
            {"label": "Bedok", "value": "Bedok"},
            {"label": "Bishan", "value": "Bishan"},
            {"label": "Bukit Batok", "value": "Bukit Batok"},
            {"label": "Bukit Merah", "value": "Bukit Merah"},
            {"label": "Bukit Panjang", "value": "Bukit Panjang"},
            {"label": "Bukit Timah", "value": "Bukit Timah"},
            {"label": "Central Area", "value": "Central Area"},
            {"label": "Choa Chu Kang", "value": "Choa Chu Kang"},
            {"label": "Clementi", "value": "Clementi"},
            {"label": "Geylang", "value": "Geylang"},
            {"label": "Hougang", "value": "Hougang"},
            {"label": "Jurong East", "value": "Jurong East"},
            {"label": "Jurong West", "value": "Jurong West"},
            {"label": "Kallang/Whampoa", "value": "Kallang"},
            {"label": "Marine Parade", "value": "Marine Parade"},
            {"label": "Pasir Ris", "value": "Pasir Ris"},
            {"label": "Punggol", "value": "Punggol"},
            {"label": "Queenstown", "value": "Queenstown"},
            {"label": "Sembawang", "value": "Sembawang"},
            {"label": "Sengkang", "value": "Sengkang"},
            {"label": "Serangoon", "value": "Serangoon"},
            {"label": "Tampines", "value": "Tampines"},
            {"label": "Toa Payoh", "value": "Toa Payoh"},
            {"label": "Woodlands", "value": "Woodlands"},
            {"label": "Yishun", "value": "Yishun"},
        ]


INSTITUTIONS = [
                    {"value": "ite", "label": "ITE"},
                    {"value": "lasalle_degree", "label": "La Salle Degree"},
                    {"value": "lasalle_diploma", "label": "La Salle Diploma"},
                    {"value": "nafa_degree", "label": "NAFA Degree"},
                    {"value": "nafa_diploma", "label": "NAFA Diploma"},
                    {"value": "nanyang_polytechnic", "label": "Nanyang Polytechnic"},
                    {"value": "ngee_ann_polytechnic", "label": "NGEE Ann Polytechnic"},
                    {"value": "nie", "label": "NIE"},
                    {"value": "ntu", "label": "NTU"},
                    {"value": "nus", "label": "NUS"},
                    {"value": "republic_polytechnic", "label": "Republic Polytechnic"},
                    {"value": "singapore_polytechnic", "label": "Singapore Polytechnic"},
                    {"value": "sit", "label": "SIT"},
                    {"value": "smu", "label": "SMU"},
                    {"value": "suss", "label": "SUSS"},
                    {"value": "sutd", "label": "SUTD"},
                    {"value": "temasek_polytechnic", "label": "Temasek Polytechnic"}
                ]


CODE_OPTUNA = """
import optuna
from catboost import CatBoostRegressor
from sklearn.metrics import mean_absolute_error

features = ['month', 'year', 'town', 'flat_type', 'street_name',
            'storey_range', 'floor_area_sqm', 'flat_model', 'lease_commence_date',
            'remaining_lease_years']

cat_features = ['town', 'flat_type', 'street_name', 'storey_range', 'flat_model']

def objective(trial):
    params = {
        'iterations': trial.suggest_int('iterations', 1000, 3000),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.1),
        'depth': trial.suggest_int('depth', 4, 10),
        'l2_leaf_reg': trial.suggest_float('l2_leaf_reg', 1, 10)
    }
    model = CatBoostRegressor(**params, verbose=0)
    model.fit(X_train, y_train, cat_features=cat_features, eval_set=(X_val, y_val), early_stopping_rounds=50)
    preds = model.predict(X_val)
    return mean_absolute_error(y_val, preds)

study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=50)
"""

CODE_TRAIN_TEST_SPLIT = """
from sklearn.model_selection import train_test_split

X = df[features]
y = df['target']

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
"""