import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import io
import base64

def encode_image(fig):
    s = io.BytesIO()
    fig.savefig(s)
    s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")

    return s

def predict(df:pd.DataFrame=None, period = 365):
    if isinstance(df, str):
        df = pd.read_csv(df)

    m = Prophet()
    m.fit(df)

    future = m.make_future_dataframe(periods=int(period))

    forecast = m.predict(future)

    return forecast.loc[::-1].head(), df

def ui_endpoint(df:pd.DataFrame=None, period = 365):
    if df is None:
        df = 'example_retail_sales.csv'
    forecast, s = predict(df=df, period = int(period))

    return [{"type": "image", "label": "prediction", "data":  {"alt": "Prophet prediction", "src": "data:image/png;base64, " + s}},
            {"type": "dataframe", "id": "dataframe", "label": "Prophet forecast", "data": forecast}]


if __name__ == "__main__":
    path = 'example_retail_sales.csv'
    df = pd.read_csv(path)
    forecast = ui_endpoint(df=df, period = 1000)
