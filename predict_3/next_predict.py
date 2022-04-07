import pandas as pd
import numpy as np

def estimate_hires(df:pd.DataFrame):
    values = df['trend'].values
    hires = np.array((values / 20000), dtype = np.int32) + np.random.randint(0,5, values.shape[0])

    dates = df['ds'].values

    new_df = pd.DataFrame()
    new_df['date'] = dates
    new_df['New hires count'] = hires

    return new_df
