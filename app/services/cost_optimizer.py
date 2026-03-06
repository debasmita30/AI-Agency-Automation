import pandas as pd

def optimize_llm_cost():

    models = pd.DataFrame({

        "model": ["small-model","medium-model","large-model"],

        "accuracy":[0.72,0.85,0.92],

        "cost":[0.002,0.01,0.03],

        "latency":[0.2,0.5,1.2]

    })

    models["efficiency"] = models["accuracy"] / models["cost"]

    best_model = models.sort_values(
        "efficiency",
        ascending=False
    ).iloc[0]

    return best_model.to_dict()