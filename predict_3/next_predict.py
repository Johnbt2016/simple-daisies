import pandas as pd

def estimate_hires(df:pd.DataFrame):
    values = df['trend'].values
    hires = int(values / 20000) + 2

    dates = df['ds'].values

    new_df = pd.DataFrame()
    new_df['date'] = dates
    new_df['New hires count'] = hires

    return new_df
