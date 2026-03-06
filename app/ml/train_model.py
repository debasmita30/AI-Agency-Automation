import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

data_path = os.path.join(BASE_DIR, "data", "training_data.csv")


data = pd.read_csv(data_path)

X = data.drop("score", axis=1)
y = data["score"]

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

model_path = os.path.join(BASE_DIR, "app", "ml", "lead_model.pkl")

joblib.dump(model, model_path)

print("Model trained successfully.")
print("Saved to:", model_path)