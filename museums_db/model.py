from sklearn.linear_model import LinearRegression
import pandas as pd


def run_regression(df):
    """
    Run linear regression on city population vs museum visitors.
    Returns model, coefficients, and R^2 score.
    """
    X = df[["population"]]
    y = df["annual_visitors"]
    model = LinearRegression()
    model.fit(X, y)
    score = model.score(X, y)
    return model, model.coef_, model.intercept_, score
