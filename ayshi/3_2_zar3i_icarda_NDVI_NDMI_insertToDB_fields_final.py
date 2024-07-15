import time
import webbrowser
import json
import requests
import datetime
import pandas as pd
import psycopg2

layer_zar3i = QgsProject.instance().mapLayersByName('zstats_FIELDS_zar3i')[0]
layer_icarda = QgsProject.instance().mapLayersByName('zstats_FIELDS_icarda')[0]

conn = psycopg2.connect(
   database="ayishi", user='developer', password='ObuEm8Ap', host='165.227.135.116', port= '5432'
)
conn.autocommit = True
cursor = conn.cursor()

command = "SET datestyle = dmy"
cursor.execute(command)
#conn.commit()

for tenant in tenants:
    
    uri = QgsDataSourceUri()
    uri.setConnection("165.227.135.116", "5432", "ayishi", "developer", "ObuEm8Ap")
    uri.setDataSource(tenant, "agriculture_fieldattribute", None, "")
    table = QgsVectorLayer(uri.uri(), "{}_agriculture_fieldattribute".format(tenant), "postgres")
    QgsProject.instance().addMapLayers([table])
    
    field_attributes=QgsVectorLayer('D:/___DEEPFACES_SERVER/zar3i_site_updates/{}/3_communesV/zstats/zstats_FIELDS_{}.gpkg'.format(dir_update,tenant),'zstats_FIELDS_{}'.format(tenant),'ogr')
    QgsProject.instance().addMapLayer(field_attributes)

    field = 'crop_risk'
    expression = '((1-"ndvi_mean")+(2-(1+"ndmi_mean"))/2)/2'
    createWKTField(field_attributes, field, expression)

    field = 'average_yield'
    expression = '5 - 5 * "crop_risk"'
    createWKTField(field_attributes, field, expression)

    field = 'harvest_forecast'
    expression = '"average_yield" * $area/10000'
    createWKTField(field_attributes, field, expression)

    field = 'area'
    expression = '$area/10000'
    createWKTField(field_attributes, field, expression)


    createJoin(table, field_attributes, idTargetLayer="id", idJoinLayer="field_id", joinLayerFields=["crop"])
    field = 'crop'
    expression = '"{}_crop"'.format(table.name())
    createWKTField(field_attributes, field, expression)

    field_attributes.selectAll()

    for feat in field_attributes.selectedFeatures():
        #df_aux = df_missingFields[df_missingFields['commune_id'] == feat['cloud_db_commune_id']]
        if not feat['ndvi_mean']:
            feat['ndvi_mean'] = -999
        if not feat['ndmi_mean']:
            feat['ndmi_mean'] = -999

        command_zar3i = "INSERT INTO {}.agriculture_fieldattribute VALUES (default,'{}',{},{},{},{},{},{},'{}',{})".format(tenant,dateToday_format, feat['ndvi_mean'], feat['ndmi_mean'], feat['harvest_forecast'], feat['area'], feat['crop_risk'], feat['id'], feat['crop'], feat['average_yield'])
        cursor.execute(command_zar3i)
        conn.commit()
        
    del table
    
conn.close()

