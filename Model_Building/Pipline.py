import pandas as pd

from Value_Score import create_value_score
from Cost_Features import cost_feature
from Market_Value import fit_market_model
from Contract_Surplus import calculate_contract_suprlus
df = pd.read_csv("data/processed_data.csv")

# Feature Engineering
df = create_value_score(df)
df = cost_feature(df)

# Salary Valuation
df, model = fit_market_model(df)

# Contract Analysis
df = calculate_contract_suprlus(df)

# Save
df.to_csv("data/model_data.csv", index=False)

print(
    df[
        [
            "Player",
            "ValueScore",
            "PredictedMarketSalary",
            "ContractSurplus"
        ]
    ].head()
)