import pydaisi as pyd
import pandas as pd

classify = pyd.Daisi("Zero Shot Text Classification")

def get_labels(df, column, candidate_labels):
    print(df)
    data_list = df[column].to_list()
    labels = [classify.compute(text = n, candidate_labels = candidate_labels) for n in data_list]
    return labels