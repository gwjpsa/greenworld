# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 14:08:42 2023

@author: joaos
"""

import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import psycopg2

tenant = 'zar3i'#'icarda' #
year = 2024 #2024
month = 6
### ATENÇÃO EDITAR MES E ANO NA QUERY
sql_query = f"""
select hist.commune_id, hist.month, avg(hist.temp) as temp_avg_series, min(hist.temp) as temp_min_series, max(hist.temp) as temp_max_series, avg(hist.precip) as precip_sum_avg_series, max(hist.precip) as precip_sum_max_series, avg(current.temp) as temp_avg_current, avg(current.precip) as precip_sum_current
from(
   	select commune_id, extract(year from date) as year, extract(month from date) as month, avg(temp_avg) as temp, sum(precip_total) as precip
   	from agriculture_communemeteo
   	where extract(year from date) < {year}
   	group by commune_id, extract(year from date), extract(month from date)
) as hist, (
	select commune_id, extract(month from date) as month, avg(temp_avg) as temp, sum(precip_total) as precip
	from agriculture_communemeteo
	where extract(year from date) = {year}
	group by commune_id, extract(month from date)
) as current
where hist.month = current.month and hist.commune_id = current.commune_id and hist.month = {month}
group by hist.commune_id, hist.month;
"""

conn = psycopg2.connect(
    database="sdb_zar3i", user='postgres', password='greenworld', host='192.168.1.72', port= '5432'
)

# conn = psycopg2.connect(
#     database="ayishi", user='developer', password='ObuEm8Ap', host='165.227.135.116', port= '5432'
# )

conn.autocommit = True
cursor = conn.cursor()

cursor.execute(sql_query.upper())
records = cursor.fetchall()
df = pd.DataFrame(records)

columns = [
    'commune_id',
    'month',
    'temp_avg_series',
    'temp_min_series',
    'temp_max_series',
    'precip_sum_avg_series',
    'precip_sum_max_series',
    'temp_avg_current',
    'precip_sum_current'
]

df.columns = columns

df = df[[    
    'month',
    'temp_avg_series',
    'temp_min_series',
    'temp_max_series',
    'precip_sum_avg_series',
    'precip_sum_max_series',
    'temp_avg_current',
    'precip_sum_current',
    'commune_id'
]]

conn.commit()
conn.close()

conn = psycopg2.connect(
    database="ayishi", user='developer', password='ObuEm8Ap', host='165.227.135.116', port= '5432'
)

conn.autocommit = True
cursor = conn.cursor()

for row in df.iterrows():
    command = "INSERT INTO {}.agriculture_weather (month, temp_avg_series, temp_min_series, temp_max_series, precip_sum_avg_series, precip_sum_max_series, temp_avg_current, precip_sum_current, commune_id, year) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {})".format(tenant, row[1]['month'], row[1]['temp_avg_series'], row[1]['temp_min_series'], row[1]['temp_max_series'], row[1]['precip_sum_avg_series'], row[1]['precip_sum_max_series'], row[1]['temp_avg_current'], row[1]['precip_sum_current'], row[1]['commune_id'], year)
    cursor.execute(command)
    conn.commit()

conn.close()



