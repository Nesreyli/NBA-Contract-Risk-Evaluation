import pandas as pd
# Salaries used from Basketball Reference

SALARY_COLUMNS = [
    "2025-26",
    "2026-27",
    "2027-28",
    "2028-29",
    "2029-30",
    "2030-31",
    "Guaranteed"
]

def load_salaries(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path, sep="\t", encoding="utf-8")
    df = df.drop(columns=["Rk"]) #Dropped for simplicity 
    df.index = range(1, len(df) + 1)

    for col in SALARY_COLUMNS:
        df[col] = (
            df[col]
            .fillna("$0")
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .replace("", "0")
            .astype(float)
        )

    df["Player"] = df["Player"].str.strip()
    return df

if __name__ == "__main__":
    df = load_salaries("Data/salaries.csv")
    print(df.head())