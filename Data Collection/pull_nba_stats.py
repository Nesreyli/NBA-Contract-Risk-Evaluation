import pandas as pd
from nba_api.stats.endpoints import LeagueDashPlayerStats

# Information of Players found through NBA API & NBA_Stats File 
def pull_player_stats() -> pd.DataFrame:

    stats = LeagueDashPlayerStats()
    df = stats.get_data_frames()[0]
    df.index = range(1, len(df) + 1)


    df = df[
        ["PLAYER_NAME",
            "AGE",
            "GP",
            "MIN",
            "PTS",
            "REB",
            "AST",
            "STL",
            "BLK",
            "TOV"
        ]
    ]

    df.columns = [
        "Player",
        "Age",
        "GP",
        "MIN",
        "PTS",
        "REB",
        "AST",
        "STL",
        "BLK",
        "TOV"
    ]

    return df


if __name__ == "__main__":

    stats_df = pull_player_stats()

    stats_df.to_csv("Data\Stats_NBA.csv", index=False, encoding="utf-8-sig")

    print(stats_df.head())