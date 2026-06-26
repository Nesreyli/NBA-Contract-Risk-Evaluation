def aggreagte_team_risk(player_df):
    return player_df.groupby("Team").agg(
        TotalSurplus    = ("ContractSurplus", "sum"),
        AvgVaR95        = ("VaR95", "mean"),
        AvgCVaR95       = ("CVaR95", "mean"),
        AvgProbNegative = ("ProbNegative", "mean"),
        PlayerCount     = ("Player", "count"),
    ).reset_index()
