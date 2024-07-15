# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import psycopg2

def getUniqueAndDuplicated(lista):
    unique = []
    duplicate = []
    for elem in lista:
        if elem not in unique:
            unique.append(elem)
        else:
            duplicate.append(elem)
    return(unique, duplicate)


path = 'C:/Users/joaos/Downloads/3732492.csv'
#path = 'D:/___DEEPFACES_SERVER/zar3i/zar3i_site/weather/2015.csv'
#path = 'D:/___DEEPFACES_SERVER/3306819.csv'

df = pd.read_csv(path)

#colunas_finais = ['STATION', 'NAME', 'LATITUDE', 'LONGITUDE', 'DATE','TMP', 'AA1']
colunas_finais = ['STATION', 'DATE','TMP', 'AA1']
badStations = [60223099999, 60160099999, 60100099999, 60200199999, 60205199999, 60127099999, 60165099999, 60270099999, 60250099999, 60275099999, 60146099999, 60120099999, 60253099999, 60178099999, 60177099999, 60146599999, 60136099999, 60338099999]
df_final = df[colunas_finais]

df_final['DATE'] = df_final['DATE'].apply(lambda x: x[:4]+x[5:7]+x[8:10])
df_final['TMP'] = df_final['TMP'].apply(lambda y: int(y[-5:-2])/10)
df_final['AA1'] = df_final['AA1'].apply(lambda z: str(z)[3:7])
df_final['AA1'] = df_final['AA1'].replace(['','9999'],'0000')
df_final['AA1'] = df_final['AA1'].apply(lambda a: int(a)/100)

stations, dump1 = getUniqueAndDuplicated(list(df_final['STATION']))
dates, dump2 = getUniqueAndDuplicated(list(df_final['DATE']))
for s in badStations:
    try:
        stations.remove(s)
    except:
        pass
resumedDf = []

#column_names = ['STATION', 'NAME', 'LATITUDE', 'LONGITUDE', 'DATE', 'AVG_TMP', 'MAX_TMP', 'MIN_TMP', 'PRECIP_TOTAL']
column_names = ['STATION', 'DATE', 'AVG_TMP', 'MAX_TMP', 'MIN_TMP', 'PRECIP_TOTAL']
c = 0
i = 0
for station in stations:
    df_station = df_final.loc[df_final['STATION'] == station]
    for date in dates:
        
        df_date_station = df_station.loc[df_station['DATE'] == date]
        if df_date_station.empty:
            i+=1
            #print(i)
            print(str(station) + '\t' + str(date))
        tmp_array = df_date_station['TMP']
        m_aux = tmp_array != 99.9
        if False in m_aux:
            print('ola')
            j1 = tmp_array
            
        try:
            tmp_nan = np.where(m_aux, tmp_array, np.NaN)
            avgTemp = round(np.nanmean(tmp_nan), 1)
            maxTemp = round(np.nanmax(tmp_nan), 1)
            minTemp = round(np.nanmin(tmp_nan), 1)
            precip = round(sum(df_date_station['AA1']), 1)
        except:
            pass
        try:
            #resumedDf.append([station, list(df_date_station['NAME'])[0], list(df_date_station['LATITUDE'])[0], list(df_date_station['LONGITUDE'])[0], date, avgTemp, maxTemp, minTemp, precip])
            resumedDf.append([station, date, avgTemp, maxTemp, minTemp, precip])
        except:
            pass

finalDf = pd.DataFrame(resumedDf)
finalDf.columns = column_names

dictStationName = {
    60252099999:{'name':'AL MASSIRA, MO','lat':30.324997,'long':-9.413067},
    60190099999:{'name':'KASBA TADLA, MO','lat':32.5333333,'long':-6.2833333},
    60195099999:{'name':'MIDELT, MO','lat':32.6833333,'long':-4.7333333},
    60106099999:{'name':'CHEFCHAOUEN, MO','lat':35.1666666,'long':-5.3},
    60280099999:{'name':'GUELMIN, MO','lat':29.0166666,'long':-10.0666666},
    60101099999:{'name':'IBN BATOUTA, MO','lat':35.726917,'long':-5.916889},
    60340099999:{'name':'NADOR AROUI, MO','lat':34.9833333,'long':-3.0166666},
    60285099999:{'name':'PLAGE BLANCHE, MO','lat':28.448194,'long':-11.161347},
    60230099999:{'name':'MENARA, MO','lat':31.606886,'long':-8.0363},
    60156099999:{'name':'MOHAMMED V, MO','lat':33.367467,'long':-7.589967},
    60060099999:{'name':'SIDI IFNI, MO','lat':29.368983,'long':-10.180267},
    60220099999:{'name':'ESSAOUIRA, MO','lat':31.399181,'long':-9.682992},
    60185099999:{'name':'SAFI, MO','lat':32.2833333,'long':-9.2333333},
    60150099999:{'name':'BASSATINE, MO','lat':33.879067,'long':-5.515125},
    60105099999:{'name':'LARACHE, MO','lat':35.15,'long':-6.1},
    60115099999:{'name':'ANGADS, MO','lat':34.78715,'long':-1.923986},
    60135099999:{'name':'SALE, MO','lat':34.051467,'long':-6.751519},
    60155099999:{'name':'ANFA, MO','lat':33.556981,'long':-7.660492},
    60200099999:{'name':'BOUARFA, MO','lat':32.5666666,'long':-1.95},
    60210099999:{'name':'MOULAY ALI CHERIF, MO','lat':31.9475,'long':-4.398333},
    60318099999:{'name':'SANIAT RMEL, MO','lat':35.594333,'long':-5.320019},
    60141099999:{'name':'SAISS, MO','lat':33.927261,'long':-4.977958},
    60191099999:{'name':'BENI MELLAL, MO','lat':32.3666666,'long':-6.4},
    60265099999:{'name':'OUARZAZATE, MO','lat':30.939053,'long':-6.909431},
    60107099999:{'name':'CHERIF EL IDRISSI, MO','lat':35.177103,'long':-3.839525}
}

finalDf['NAME'] = [dictStationName[r['STATION']]['name'] for i,r in finalDf.iterrows()]
finalDf['LAT'] = [dictStationName[r['STATION']]['lat'] for i,r in finalDf.iterrows()]
finalDf['LONG'] = [dictStationName[r['STATION']]['long'] for i,r in finalDf.iterrows()]
finalDf = finalDf[finalDf['DATE'] > '20240514']
#finalDf.to_csv('D:/___DEEPFACES_SERVER/zar3i/zar3i_site/202305d/tabela_missingValues.csv')

finalDf.to_csv('S:/zar3i_site/Weather/20240621_20240630_clean.csv') ## <--------- EDITAR
#engine = create_engine('postgresql://postgres:greenworld@192.168.1.71:5432/sdb_zar3i')
#finalDf.to_sql('temp_stations', engine)
#GDD = ((tMin + tMax )/ 2) - 4.5
#%%
conn = psycopg2.connect(
    database="sdb_zar3i", user='postgres', password='greenworld', host='192.168.1.72', port= '5432'
)
conn.autocommit = True
cursor = conn.cursor()
for row in finalDf.iterrows():
    try:
        command = "INSERT INTO temp_stations VALUES (default, default,{},'{}',{},{},{},{},{},{},{})".format(row[1]['STATION'], row[1]['NAME'], row[1]['LAT'], row[1]['LONG'], row[1]['DATE'], row[1]['AVG_TMP'], row[1]['MAX_TMP'], row[1]['MIN_TMP'], row[1]['PRECIP_TOTAL'])
        cursor.execute(command)
        conn.commit()
    except:
        pass
conn.close()