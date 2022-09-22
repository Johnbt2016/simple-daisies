import os
import pandas as pd

def get_env_var():
    res =  os.environ

    df = pd.DataFrame()
    df['vars'] = [k for k, v in res.items()]
    df['vals'] = [v for k, v in res.items()]

    return df


if __name__ == "__main__":
    res = get_env_var()

    print(res)