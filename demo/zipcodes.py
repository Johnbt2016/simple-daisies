

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

def latlon_per_zip_code(store_zips):
    futures = [geo.address_to_coordinates_(address=str(z) + ',USA') for z in store_zips]
    while futures[-1].get_status() == 'RUNNING':
        time.sleep(0.1)
    result = [res.value() for res in futures]

    return result

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

    result = latlon_per_zip_code(zip_codes)
    print(result)

    pickle.dump(result, open( "latlon.p", "wb" ))

data_prep()