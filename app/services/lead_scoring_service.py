import warnings
warnings.filterwarnings("ignore")
import joblib
import numpy as np

model = joblib.load("app/ml/lead_model.pkl")

def predict_lead_score(company_size, budget, urgency, ai_interest):
    features = np.array([
        [company_size, budget, urgency, ai_interest]
    ])
    score = model.predict(features)[0]
    return round(score, 2)
