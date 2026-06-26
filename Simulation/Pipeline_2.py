import pandas as pd
from Monte_Carlo import run_monte_carlo       
from Risk_Aggregator import aggreagte_team_risk

df = pd.read_csv("data/model_data.csv")
player_risk = run_monte_carlo(df)

# Merge ValueScore and ValuePerMillion in before saving
cols_to_merge = ["Player", "ValueScore", "ValuePerMillion"]
player_risk = player_risk.merge(df[cols_to_merge], on="Player", how="left")

player_risk.to_csv("data/player_risk.csv", index=False)