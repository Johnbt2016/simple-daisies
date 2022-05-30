import requests
import pandas as pd
import streamlit as st

API_KEY="oNfQ09TCevKt99acGiRK9wPjtCul6TRlf524BCzKS5ZJmrF9w-FaAPBe88T5_KVkmtCkT3gTExvUJJcmUvV-W-_iDIQZgnlhr2fMlW1revgVzkBkjUBBH1w4nIx1YnYx"

def get_reviews(term="korean", location="Houston"):

    r = requests.get(f"https://api.yelp.com/v3/businesses/search?term={term}&location={location}", headers={"Authorization": f"Bearer {API_KEY}"})

    bus_ids = [{"id": x["id"], "name": x["name"]} for x in r.json()["businesses"][:5]]

    raw_data = []
    for business in bus_ids:
        b_id = business["id"]
        r = requests.get(f"https://api.yelp.com/v3/businesses/{b_id}/reviews", headers={"Authorization": "Bearer oNfQ09TCevKt99acGiRK9wPjtCul6TRlf524BCzKS5ZJmrF9w-FaAPBe88T5_KVkmtCkT3gTExvUJJcmUvV-W-_iDIQZgnlhr2fMlW1revgVzkBkjUBBH1w4nIx1YnYx"})
        res = r.json()

        raw_data.append([business, res])
    
    review_text = []
    for data in raw_data:
        business = data[0]
        res = data[1]
        for review in res["reviews"]:
            review_text.append(
                                {"name": business["name"], 
                                "url": review["url"], 
                                "rating": review["rating"], 
                                "review": review["text"]}
                                )
    
    df = pd.DataFrame(review_text)

    return df

def st_ui():
    st.title("Restaurants reviews from Yelp")

    term = st.sidebar.text_input("Style", "korean")
    location = st.sidebar.text_input("Location", "Houston")

    df = get_reviews(term, location)

    st.dataframe(df)

if __name__ == "__main__":
    st_ui()