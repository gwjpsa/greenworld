import time
import webbrowser
import json
import requests
import datetime
import pandas as pd
import psycopg2
#exec(open('D:/___DEEPFACES_SERVER/zar3i/scripts/0_greenWorldPyQgis.py').read())
conn = psycopg2.connect(
   database="ayishi", user='developer', password='ObuEm8Ap', host='165.227.135.116', port= '5432'
)
conn.autocommit = True
cursor = conn.cursor()

command = "SET datestyle = dmy"
cursor.execute(command)
conn.commit()

command = "select commune_id, available_agriculture_land, planted_area from zar3i.agriculture_communeattribute where date = '31/03/2023'"
row = cursor.execute(command)
rows = cursor.fetchall()
conn.commit()

conn.close()

colunas = ['commune_id', 'available_agriculture_land', 'planted_area']
df_missingFields = pd.DataFrame(rows)
df_missingFields.columns = colunas