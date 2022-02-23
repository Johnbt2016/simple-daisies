import pandas as pd

def convert(json_out, field = "title"):
    data = [o[field] for o in json_out]
    df = pd.DataFrame([{"id": i, "description": t} for i, t in enumerate(data)])

    return df
