from GoogleNews import GoogleNews
from datetime import datetime
import pickle
import pandas as pd

def get_news(query, num=10):
    print('paramters: ', query, num)

    googlenews = GoogleNews(lang='en', region='US', period="1d")

    start = datetime.now()
    googlenews.get_news(query)
    print(f"get news time: {datetime.now() - start}")
    
    print(f"total results: {len(googlenews.results())}")
    
    data = googlenews.results()[:int(num)]
    for r in data:
        if r["datetime"] is None:
            r["datetime"] = datetime.now().strftime("%m/%d/%Y, %H")
        else:
            r["datetime"] = r["datetime"].strftime("%m/%d/%Y, %H")
    
    df = pd.DataFrame(data) 

    return df


    # return {"result": data}