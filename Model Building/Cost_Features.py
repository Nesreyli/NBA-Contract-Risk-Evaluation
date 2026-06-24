import pandas as pd

def cost_feature(df):
    #Higher Number gives efficent contract
    df["ValuePerMillion"] = df["ValueScore"] / (df["2025-26"] / 1_000_000)

    #Useful for Comparing Sizes of Contracts 
    df["GuarnteedPerYear"] = ( df["Guaranteed"]/ df["YearsRemaining"])

    return df 