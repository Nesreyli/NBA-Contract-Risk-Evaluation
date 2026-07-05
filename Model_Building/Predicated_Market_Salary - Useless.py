import pandas as pd 
from sklearn.linear_model import LinearRegression


def predict_market_salary(df):
    X = df[["Age",
            "PPG",
            "RPG",
            "APG",
            "MPG"]]
    
    y = df["2025-26"]

    model = LinearRegression()
    model.fit(X, y)

    df["PredictedMarketSalary"] = model.predict(X)
    df["ValueRatio"] = (df["PredictedMarketSalary"]/df["2025-26"])

    df["ContractSurplus"] = (df["PredictedMarketSalary"] - df["2025-26"])

    return df,model

if __name__ == "__main__":

    # Load processed data
    df = pd.read_csv("data/processed_data.csv")

    # Run model
    df, model = predict_market_salary(df)

    # Save results
    df.to_csv("data/banana.csv", index=False)

    # Show top players
    print(
        df[
            [
                "Player",
                "PredictedMarketSalary",
                "ValueRatio",
                "ContractSurplus"
            ]
        ]
        .sort_values(
            "PredictedMarketSalary",
            ascending=False
        )
        .head(20)
    )
      