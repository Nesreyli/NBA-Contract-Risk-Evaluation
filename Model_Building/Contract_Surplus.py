import pandas as pd

def calculate_contract_suprlus(df):
    df["ContractSurplus"] =df["PredictedMarketSalary"] - df["2025-26"]
    return df