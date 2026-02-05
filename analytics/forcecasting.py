from statsmodels.tsa.arima.model import ARIMA

def forecast(series, steps=6):
    series = series.dropna()
    model = ARIMA(series, order=(1,1,1))
    fitted = model.fit()
    return fitted.forecast(steps=steps).tolist()
