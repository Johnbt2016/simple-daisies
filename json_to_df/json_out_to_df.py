import pandas as pd
import pickle

def convert(json_out, field = "title"):
    data = [o[field] for o in json_out]
    df = [{"id": i, "description": t} for i, t in enumerate(data)]

    return df
