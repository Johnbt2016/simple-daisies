
import pandas as pd
import numpy as np
import pickle

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

    pickle.dump(store_dataset, open( "store_dataset.p", "wb" ))
    pickle.dump(zip_codes, open( "zip_codes.p", "wb" ))
    pickle.dump(stores_names, open( "stores_names.p", "wb" ))
    pickle.dump(zip_dict, open( "zip_dict.p", "wb" ))



    

    
    return store_dataset, product_dataset, zip_codes, stores_names, zip_dict

data_prep()