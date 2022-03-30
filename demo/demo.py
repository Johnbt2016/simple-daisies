

from pydaisi import Daisi

daisi_prophet = Daisi("Simple Prophet")
geo = Daisi("GeoEncoder")


import streamlit as st

import pandas as pd
import io
import base64
import numpy as np
import PIL
from PIL import Image
import pydeck as pdk
import time
import pickle

def hello(name):
    return name
@st.cache
def data_prep():
    store_dataset = pd.read_csv("daily_sales_by_store-2.csv")
    product_dataset = pd.read_csv("daily_sales_by_product_category.csv")

    store_dataset.rename(columns={'Date':'ds'}, inplace=True)
    store_dataset.rename(columns={'Sale_Dollars':'y'}, inplace=True)

    product_dataset.rename(columns={'Date':'ds'}, inplace=True)
    product_dataset.rename(columns={'Sale_Dollars':'y'}, inplace=True)

    zip_codes = np.asarray(store_dataset['ZipCode'].tolist())
    print(zip_codes)
    zip_codes = np.unique(zip_codes)
    zip_codes= np.array(zip_codes[~np.isnan(zip_codes)], dtype = np.int32)
    print(zip_codes)

    zip_codes = np.insert(zip_codes, -1, 0)
    
        
    stores_names = ['Kum & Go', 'Casey', 'Fareway', 'Quik Trip', 'Walgreens', 'Hy-Vee', 'Wal-Mart', 'Smokin\' Joe', 'Sam\'s Club']
    # new_names = [s if s in row['StoreName'] else 'other' for _, row in store_dataset.iterrows() for s in stores_names]
    new_names = []
    for _, row in store_dataset.iterrows():
        exit = False
        for s in stores_names:
            if not exit:
                if s in row['StoreName']:
                    new_names.append(s)
                    exit = True
        if not exit:
            new_names.append('other')



    store_dataset['CleanNames'] = new_names

    # result = latlon_per_zip_code(zip_codes)

    result = pickle.load(open( "latlon.p", "rb" ))
    # print(result)
    zip_dict = dict()
    for i, z in enumerate(zip_codes):
        print(i, z)
        try:
            zip_dict[z] = {"lat": result[i]['latitude'], "lon": result[i]['longitude']}
        except:
            zip_dict[z] = {"lat": 0.0, "lon": 0.0}
            print("problem with ", i, z, result[i])

    lat = []
    lon = []


    for _, row in store_dataset.iterrows():
        try:
            z = int(row['ZipCode'])
            lat.append(zip_dict[z]['lat'])
            lon.append(zip_dict[z]['lon'])
        except:
            lat.append(np.nan)
            lon.append(np.nan)
    
    store_dataset['lat'] = lat
    store_dataset['lon'] = lon



    
    return store_dataset, product_dataset, zip_codes, stores_names, zip_dict


def filter_df(store_dataset, store_choice, zip_choice):

    zip_select = (store_dataset['ZipCode'] == zip_choice)
    store_select = (store_dataset['CleanNames'] == store_choice)
    if len(zip_select.loc[zip_select == True]) + len(store_select.loc[store_select == True]) > 0:
        filter = (zip_select & store_select)
        message = "Forecasting for zip code " + str(zip_choice) + " and store " + store_choice
        if zip_choice == 0:
            zip_select = None
            filter = store_select
            message = "Forecasting for store " + store_choice + " in all zip codes"
        if store_choice == 'All Stores':
            store_select = None
            filter = zip_select
            print("Filter", filter)
            message = "Forecasting for all stores in zip code " + str(zip_choice)
        df = store_dataset.loc[filter]
    else:
        df = store_dataset
        message = "Forecasting for all stores in all zip codes"

    return df, message

@st.cache
def get_all_adresses(df):

    addresses = [row['Address'] + ',' + row['City'] + ',' + row['ZipCode'] for i, row in df.iterrows()]
    print(len(addresses))
    futures = [geo.address_to_coordinates_(address=a) for a in addresses]
    while futures[-1].get_status() == 'RUNNING':
        time.sleep(0.1)
    result = [latlon.value() for latlon in futures]
    lat = [result['latitude'] for latlon in futures]
    lon = [result['longitude'] for latlon in futures]

    df['lat'] = lat
    df['lon'] = lon

    return df

def get_store_zips(df):
    store_zips = np.asarray(df['ZipCode'].tolist())
    store_zips = np.unique(store_zips)
    store_zips= np.array(store_zips[~np.isnan(store_zips)], dtype = np.int32)
    print(store_zips)
    return store_zips

def latlon_per_zip_code(store_zips):
    futures = [geo.address_to_coordinates_(address=str(z) + ',USA') for z in store_zips]
    while futures[-1].get_status() == 'RUNNING':
        time.sleep(0.1)
    result = [res.value() for res in futures]

    return result

def predict_per_zip_code(df, store_choice, store_zips, period):
    dfs = []
    for z in store_zips:
        d, _ = filter_df(df, store_choice, z)
        dfs.append(d)

    futures = [daisi_prophet.predict_(d, period = period) for d in dfs]
    while futures[-1].get_status() == 'RUNNING':
        time.sleep(0.1)
    result = []
    for i, res in enumerate(futures):
        try:
            result.append([store_zips[i], np.sum(np.array(res[0]['yhat']).flatten())])
        except:
            result.append([store_zips[i],[0]])

    return result

def get_geo_df(per_zip_code, lat_lon, zip_dict):

    lat = [latlon['latitude'] for latlon in lat_lon]
    lon = [latlon['longitude'] for latlon in lat_lon]
    data = [np.sum(np.array(res[0]['yhat']).flatten()) for res in per_zip_code]
    geo_df = pd.DataFrame()
    geo_df['lat'] = lat
    geo_df['lon'] = lon
    geo_df['data'] = data

    return geo_df

def get_geo_df_all(store_zips, zip_dict):

    lat = [float(zip_dict[z]['lat']) for z in store_zips]
    lon = [float(zip_dict[z]['lon']) for z in store_zips]
    geo_df = pd.DataFrame()
    geo_df['lat'] = lat
    geo_df['lon'] = lon
    geo_df['data'] = 100
    geo_df['zip'] = store_zips

    return geo_df

def data_load():
    store_dataset =  pickle.load(open( "store_dataset.p", "rb" ))
    zip_codes =  pickle.load(open( "zip_codes.p", "rb" ))
    stores_names = pickle.load(open( "stores_names.p", "rb" ))
    zip_dict = pickle.load(open( "zip_dict.p", "rb" ))

    return store_dataset, zip_codes, stores_names, zip_dict

def st_ui():
    st.set_page_config(layout = "wide")

    
    store_dataset, zip_codes, stores_names, zip_dict = data_load()
    store_choice = st.sidebar.selectbox("Select a store chain", stores_names)
    df_store, message = filter_df(store_dataset, store_choice, zip_choice=0)
    store_zips = get_store_zips(df_store)
    z_options = store_zips
    zip_choice = st.sidebar.selectbox("Select a Zip Code", z_options)

    st.title("Retail Volume forecast - " + store_choice)


    period = st.sidebar.slider("Select a forecast period (days)", 100, 1000, 365)

    df, message = filter_df(df_store, store_choice, zip_choice)
    
    st.markdown(message + " with [Daisi(\"Volume Forecast\")](https://app.daisi.io/daisies/f2e42e79-c785-4170-8719-8a88d5b80205/info) :blossom:")

    col1, col2 = st.columns(2)
    with col1:
        st.header(store_choice + " stores items volume forecast for Zip Code " + str(zip_choice))
        if len(df) > 0:
            res = daisi_prophet.predict(df = df, period = period)
        
            imgdata = base64.b64decode(res.value()[1])
            image = Image.open(io.BytesIO(imgdata)).convert('RGBA')
            st.image(image)

            st.dataframe(res.value()[0])
        else:
            st.write("Empty selection. Review your filters")
    
    # per_zip_code = predict_per_zip_code(df_store, store_choice, store_zips, 365)
    # lat_lon = latlon_per_zip_code(store_zips)
    # geo_df = get_geo_df(per_zip_code, df_store, zip_dict) 
    with col2:
        st.header(store_choice + " Stores locations - Highlight on " + str(zip_choice))
        geo_df = get_geo_df_all(store_zips, zip_dict)
        filtered_geo = geo_df.loc[geo_df['zip'] == zip_choice]

        print(geo_df)
        for _, row in geo_df.iterrows():
            print(row)
        st.pydeck_chart(
            pdk.Deck(map_style='mapbox://styles/mapbox/light-v8',
                    initial_view_state=pdk.ViewState(latitude=float(zip_dict[zip_choice]['lat']),longitude=float(zip_dict[zip_choice]['lon']),zoom=8,pitch=0),
                    layers=[pdk.Layer( "ScatterplotLayer",geo_df,
        pickable=True,
        opacity=1.0,
        stroked=True,
        filled=True,
        radius_scale=6,
        radius_min_pixels=1,
        radius_max_pixels=100,
        line_width_min_pixels=1,
        get_position=['lon', 'lat'],
        get_radius='data',
        get_fill_color=[255, 140, 0],
        get_line_color=[0, 0, 0]
    ),
    pdk.Layer( "ScatterplotLayer",filtered_geo,
        pickable=True,
        opacity=1.0,
        stroked=True,
        filled=True,
        radius_scale=6,
        radius_min_pixels=1,
        radius_max_pixels=100,
        line_width_min_pixels=1,
        get_position=['lon', 'lat'],
        get_radius=500,
        get_fill_color=[0, 255, 0],
        get_line_color=[0, 0, 0]
    )]))
    

    
# st_ui()
if __name__ == "__main__":
    st_ui()