import time
import webbrowser
import json
import requests
import datetime
import pandas as pd
import psycopg2



layerGPS = QgsVectorLayer('D:/___DEEPFACES_SERVER/zar3i_site_updates/'+dir_update+'/3_communesV/zstats/zstats_final.gpkg|layername=zstats_final','zstats_final','ogr')
QgsProject.instance().addMapLayer(layerGPS)
#layerGPS = QgsProject.instance().mapLayersByName('layerGPS')[0]
layerGPS.selectAll()

field = 'crop_risk'
expression = '((1-"NDVI_mean")+(2-(1+"NDMI_mean"))/2)/2'
createWKTField(layerGPS, field, expression)

field = 'average_yield'
expression = '5 - 5 * "crop_risk"'
createWKTField(layerGPS, field, expression)

field = 'harvest_forecast'
expression = '"average_yield" * $area/10000'
createWKTField(layerGPS, field, expression)

field = 'area'
expression = '$area/10000'
createWKTField(layerGPS, field, expression)

# datetoday = datetime.datetime.now().date()
# dateToday_format = str(datetoday.day) + '/' + str(datetoday.month) + '/' + str(datetoday.year) 
conn = psycopg2.connect(
   database="ayishi", user='developer', password='ObuEm8Ap', host='165.227.135.116', port= '5432'
)
conn.autocommit = True
cursor = conn.cursor()

command = "SET datestyle = dmy"
cursor.execute(command)
conn.commit()

for feat in layerGPS.selectedFeatures():
    df_aux = df_missingFields[df_missingFields['commune_id'] == feat['id']] #cloud_db_commune_id
    command1 = "INSERT INTO zar3i.agriculture_communeattribute VALUES (default,'{}',{},{},{},{},{},{},{})".format(dateToday_format, feat['NDVI_mean'], feat['NDMI_mean'], float(df_aux['available_agriculture_land']), float(df_aux['planted_area']), feat['crop_risk'], feat['id'], feat['average_yield'])
    command2 = "INSERT INTO icarda.agriculture_communeattribute VALUES (default,'{}',{},{},{},{},{},{},{})".format(dateToday_format, feat['NDVI_mean'], feat['NDMI_mean'], float(df_aux['available_agriculture_land']), float(df_aux['planted_area']), feat['crop_risk'], feat['id'], feat['average_yield'])
    cursor.execute(command1)
    cursor.execute(command2)
    conn.commit()
conn.close()