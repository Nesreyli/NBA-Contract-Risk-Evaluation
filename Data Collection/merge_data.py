import pandas as pd

def merge_data(salary_df: pd.DataFrame, stats_df: pd.DataFrame) -> pd.DataFrame:
    merged = pd.merge(salary_df, stats_df, on="Player", how="inner")
    merged.index = range(1, len(merged) + 1)

    return merged

if __name__ == "__main__":

    salary_df = pd.read_csv("Data\salaries.csv", sep="\t", encoding="utf-8")
    salary_df = salary_df.drop(columns=["Rk"])
    stats_df = pd.read_csv("Data\Stats_NBA.csv")

    merged_df = merge_data(salary_df, stats_df)
    merged_df.to_csv("Data/processed_data.csv", index=False)

    print(merged_df.head())