# src/data/create_processed_data.py

import pandas as pd

from load_salaries import load_salaries
from pull_nba_stats import pull_player_stats
from merge_data import merge_data


def create_processed_data():

    # Loading Found Data 
    salary_df = load_salaries( "data/salaries.csv")
    stats_df = pull_player_stats()
    merged_df = merge_data(salary_df, stats_df)


    # Adjust Season Stats into Per Game Stats
    merged_df["PPG"] = (merged_df["PTS"] / merged_df["GP"])
    merged_df["RPG"] = (merged_df["REB"] / merged_df["GP"])
    merged_df["APG"] = (merged_df["AST"] / merged_df["GP"])
    merged_df["MPG"] = (merged_df["MIN"] / merged_df["GP"])

    # For Contracts ending early puts 0.0 as placeholder later yers 
    merged_df["YearsRemaining"] = (
    (merged_df["2026-27"] > 0).astype(int)
    + (merged_df["2027-28"] > 0).astype(int)
    + (merged_df["2028-29"] > 0).astype(int)
    + (merged_df["2029-30"] > 0).astype(int)
    + (merged_df["2030-31"] > 0).astype(int)
    + 1
)

    # Saving Data 
    merged_df.to_csv("data/processed_data.csv", index=False)
    return merged_df


if __name__ == "__main__":
    df = create_processed_data()
    print(df.head())