import googlemaps
import pandas as pd
import numpy as np
from ruteo.haversine import haversine
import time


def get_distances(origins,customers,typeM,key_googlemaps):
    destinations = origins.copy()
    len_origins = len(customers)
    len_destinations = len_origins
    df = pd.DataFrame(0, index=np.arange(len_origins*len_destinations),columns=['origins','destinations'],dtype='object')
    df_f = pd.DataFrame(0, index=np.arange(len_origins*len_destinations),columns=['origins','destinations'],dtype='object')
    k=0
    for i in range(len(customers)):
        for j in range(len(customers)):
            df.iloc[k,0] = origins[i]
            df.iloc[k,1] = destinations[j]
    
            df_f.iloc[k,0] = customers[i]
            df_f.iloc[k,1] = customers[j]
    
            k+=1
    def get_gmaps_distance(df):
        if df['origins'] != df['destinations']:
            result = gmaps.distance_matrix(df['origins'], df['destinations'], mode='driving')
            status = result['rows'][0]['elements'][0]['status']
        else:
            result = 0 
            status ="NULL"
    
        if status == "OK":
            KM = int(result['rows'][0]['elements'][0]['distance']['value'] / 1000)
            Time = (result['rows'][0]['elements'][0]['duration']['value']/3600)
        else:
            KM = haversine(df['origins'][1],df['origins'][0],df['destinations'][1],df['destinations'][0])*1.5
            Time = KM/35 #average speed of 35km/h 
    
        return pd.Series([KM,Time])
    #print('Obtaining distances from API google...')
    gmaps = googlemaps.Client(key=key_googlemaps)
    #start_time = time.time()
    df_f[["distance (Km)","Time (H)"]] = df.apply(get_gmaps_distance, axis=1) #To get distances
    #print("Run time API google:")
    #print("--- %s segundos ---" % (time.time() - start_time))
    if typeM == 'Time':
        df_f = df_f.pivot_table(index ='origins', columns ='destinations', values =["Time (H)"], sort=False).reset_index()
    else:
        df_f = df_f.pivot_table(index ='origins', columns ='destinations', values =["distance (Km)"], sort=False).reset_index()
    
    df_f.columns = df_f.columns.droplevel(0)
    df_f = df_f.rename_axis(None, axis=1)
    df_f = df_f.drop(df_f.columns[0], axis=1)

    df_f = df_f.to_numpy()
    return df_f

