from statsmodels.tsa.arima.model import ARIMA


def forecast(series, steps=6):
    """
    Simple ARIMA-based time series forecast
    """
    series = series.dropna()

    if len(series) < 10:
        return ["Not enough data for forecasting"]

    model = ARIMA(series, order=(1, 1, 1))
    fitted_model = model.fit()
    forecast_values = fitted_model.forecast(steps=steps)

    return forecast_values.tolist()
