import numpy as np
import pandas as pd

def run_monte_carlo(df, n_sims = 10_000, seed=42):
    rng = np.random.default_rng(seed)
    residual_std = (df["PredictedMarketSalary"] - df["2025-26"]).std()
    results = []

    for _, row in df.iterrows():
        sims = rng.normal(loc=row["ContractSurplus"], scale=residual_std, size=n_sims)
        results.append({
            "Player":           row["Player"],
            "Team":             row["Team"],
            "ContractSurplus":  row["ContractSurplus"],
            "ExpectedLoss":     sims[sims < 0].mean() if (sims < 0).any() else 0,
            "VaR95":            np.percentile(sims, 5),
            "CVaR95":           sims[sims <= np.percentile(sims, 5)].mean(),
            "ProbNegative":     (sims < 0).mean(),
        })
    return pd.DataFrame(results)
