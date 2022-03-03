import pandas as pd

def nlp_df(df):
    if 'title' in df.keys():
        data = df['title'].tolist()
        papers = pd.DataFrame([{"id": i, "description": t} for i, t in enumerate(data)])
    else:
        papers = df
    
    return papers
    

