from sklearn.linear_model import LinearRegression

def  fit_market_model(df):
    X = df[["ValueScore"]]
    y = df["2025-26"]

    model = LinearRegression()
    model.fit(X, y)
    df["PredictedMarketSalary"] = model.predict(X)

    return df, model