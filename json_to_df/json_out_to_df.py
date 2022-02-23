import pandas as pd
import pickle


def convert(json_out, field = "title"):
    data = [o[field] for o in json_out[0]['result']]
    df = pd.DataFrame([{"id": i, "description": t} for i, t in enumerate(data)])

    return df


if __name__ == "__main__":
    df = convert(json_out=gn)
    print(df)