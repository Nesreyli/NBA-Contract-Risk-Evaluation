import numpy as np
import pandas as pd

def run_monte_carlo(df, n_sims = 10_000, seed=42):
    rng = np.random.default_rng(seed)
    residual_std = (df["PredictedMarketSalary"] - df["2025-26"]).std()
    results = []

    for _, row in df.iterrows():  
        age = row["Age"]
        # Higher Upside on Younger      
        if age < 25:
            age_factor = 1.1
        # Prime of NBA careers
        elif age < 30:
            age_factor = 1.0
        # Early signs of Decline in NBA careers
        elif age < 33:
            age_factor = 1.15
        # Outside of Prime for Careers
        else:
            age_factor = 1.35

        # Fewer Games played presents Uncertanity in Health 
        gp_factor = 1 + (1 - row["GP"] / 82) * 0.3
        std_i = residual_std * age_factor * gp_factor

        sims = rng.normal(loc=row["ContractSurplus"], scale=std_i, size=n_sims)

        results.append({
            "Player":          row["Player"],
            "Team":            row["Team"],
            "ContractSurplus": row["ContractSurplus"],
            "ExpectedLoss":    sims[sims < 0].mean() if (sims < 0).any() else np.nan,
            "VaR95":           np.percentile(sims, 5),
            "CVaR95":          sims[sims <= np.percentile(sims, 5)].mean(),
            "ProbNegative":    (sims < 0).mean(),
        })

    return pd.DataFrame(results)
