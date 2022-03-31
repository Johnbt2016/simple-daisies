import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from matplotlib.backends.backend_agg import RendererAgg
import time
import streamlit as st
from pydaisi import Daisi

_lock = RendererAgg.lock

news = Daisi("GoogleNews")
classification = Daisi("Zero Shot Text Classification")

def news_f(query, nb = 10):
    #Daisi call to query Google News
    n = news.get_news(query = query, num = nb)
    print(n.value)
    data = n.value['title'].tolist()
    print([d for d in data])
    return data, n.value


def plot_data(n_scores):
    n_scores = 100 * np.array(n_scores)
    fig, ax = plt.subplots(figsize = (10, 8))
    positivity = (n_scores < 50).sum()
    print(positivity)
    if positivity > n_scores.shape[0] / 2:
        color = "#82C442"
    else:
        color = "#E42626"

    ax.hist(n_scores, bins =10, color = color) 
    ax.set_title("<-- Positive sentiment ----- Negative sentiment -->") 
    
    return fig


def streamlit_ui():
    st.title("Google News - Sentiment Analysis")
    query = st.sidebar.text_input('query', "Apple")
    nb_result = st.sidebar.slider("Number of results", 10, 50, 15)
    st.markdown("Querying news about **" + query + "** with [Daisi(\"GoogleNews\")](https://app.daisi.io/daisies/62afa319-4408-49c0-ab64-38563f9cea2a/info) :blossom:")
    
    data, df = news_f(query, nb = nb_result)

    st.success("News results available")

    st.markdown("Classifying news with [Daisi(\"Zero Shot Text Classification\")](https://app.daisi.io/daisies/237587e0-7c47-4a4f-afad-80370c8e98a4/info) :blossom:")

    my_bar = st.progress(0)
    all = []
    for i in range(len(data)):
        p = int(100*(i+1)/len(data))
        my_bar.progress(p)
        #Asynchronous Daisi call to classify each Google News result
        all.append(classification.compute_(text=data[i], candidate_labels="positive, negative"))
        time.sleep(0.1)

    r = all[-1]
    with st.spinner('Wait for it...'):
        if r.get_status() == "RUNNING":
            time.sleep(3)
    st.success("Classification completed")

    st.write("Fetching results")
    results = []
    my_bar = st.progress(0)
     #Fetching Daisi executions results (could be parallelized)
    for i in range(len(all)):
        p = int(100*(i+1)/len(all))
        my_bar.progress(p)
        try:
            results.append(all[i].value)
        except:
            continue
    
    n_index = [aa['result']['labels'].index('negative') for aa in results]
    scores = [v['result']['scores'] for v in results]
    n_scores = [s[n_index[ii]] for ii, s in enumerate(scores)]

    with _lock:

        fig = plot_data(n_scores)
        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches='tight', transparent = True)
        st.image(buf, use_column_width=False)

    st.dataframe(df)


if __name__ == "__main__":
    streamlit_ui()



