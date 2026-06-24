import pandas as pd

def create_value_score(df: pd.DataFrame) -> pd.DataFrame:
    df["ValueScore"] = (
        df["PPG"]
        + 1.2 * df["RPG"]
        + 1.5 * df["APG"]
        + 3.0 * (df["STL"] / df["GP"])
        + 3.0 * (df["BLK"] / df["GP"])
        - (df["TOV"] / df["GP"])
    )
    return df 