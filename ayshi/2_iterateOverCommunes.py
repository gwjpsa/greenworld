import datetime
import os

#communesLayer = QgsProject.instance().mapLayersByName('agro_commune')[0]

communesLayer = QgsVectorLayer(r"D:\___DEEPFACES_SERVER\zar3i_aux\agro_commune.gpkg", 'agro_commune', 'ogr')
QgsProject.instance().addMapLayer(communesLayer, True)
communesLayer.setSubsetString('')

AOI_diff_water_roads_rails_Layer = QgsVectorLayer(r"D:\___DEEPFACES_SERVER\zar3i_aux\AOI_diff_water_roads_rails.gpkg", 'AOI_diff_water_roads_rails', 'ogr')
QgsProject.instance().addMapLayer(AOI_diff_water_roads_rails_Layer, True)

pathNDMI = 'D:/___DEEPFACES_SERVER/zar3i_site_updates/'+dir_update+'/2_merge/NDMI.tif'
pathNDVI = 'D:/___DEEPFACES_SERVER/zar3i_site_updates/'+dir_update+'/2_merge/NDVI.tif'

pathOutNDMI = 'D:/___DEEPFACES_SERVER/zar3i_site_updates/'+dir_update+'/3_communesV/NDMI/'
pathOutNDVI = 'D:/___DEEPFACES_SERVER/zar3i_site_updates/'+dir_update+'/3_communesV/NDVI/'
pathOutFinal = 'D:/___DEEPFACES_SERVER/zar3i_site_updates/'+dir_update+'/3_communesV/zstats/'

jobs = {
     1:"'0274-0340'", 
     2:"'0341-0390'", 
     3:"'0391-0440'",
     4:"'0441-0490'", 
     5:"'0491-0540'", 
     6:"'0541-0590'", 
     7:"'0591-0640'", 
     8:"'0641-0690'", 
     9:"'0691-0740'", 
    10:"'0741-0790'",
    11:"'0791-0840'",
    12:"'0841-0890'",
    13:"'0891-0940'",
    14:"'0941-0990'",
    15:"'0991-1040'",
    16:"'1041-1090'",
    17:"'1091-1152'"
}

#job_it =1 #<------------------------------------ ATENÇÃO

varAux =jobs[job_it]
#varAux ='lacunas2'
communesLayer.setSubsetString('"id" >= ' + varAux[1:5] + ' AND "id" <= ' + varAux[6:10])

fileOutputName = 'communes_zonalStats_NDMI_NDVI_{}.gpkg'.format(varAux)
#exec(open('C:/Users/joaos/OneDrive/Ambiente de Trabalho/QGIS_TESTES/greenWorldPyQgis.py').read()) ### este path tem de ser editado
deleteTemporaryLayers()

communes_reprojected = processing.run("native:reprojectlayer", {
    'INPUT':communesLayer,
    'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:32629'),
    'OPERATION':'+proj=pipeline +step +proj=unitconvert +xy_in=deg +xy_out=rad +step +proj=utm +zone=29 +ellps=WGS84',
    'OUTPUT':'TEMPORARY_OUTPUT'
})['OUTPUT']
QgsProject.instance().addMapLayer(communes_reprojected, False)

#communes_reprojected.selectAll()
#for f in communes_reprojected.selectedFeatures():
    
distance = 20 # 20 m

communes_buffered = processing.run("native:buffer", {
    'INPUT':QgsProcessingFeatureSourceDefinition(
        communes_reprojected.source(),
        selectedFeaturesOnly=False,
        featureLimit=-1,
        flags=QgsProcessingFeatureSourceDefinition.FlagCreateIndividualOutputPerInputFeature, ## flag para iterar sobre cada feature
        geometryCheck=QgsFeatureRequest.GeometryAbortOnInvalid
    ),
    'DISTANCE':distance,
    'SEGMENTS':5,
    'END_CAP_STYLE':0,
    'JOIN_STYLE':0,
    'MITER_LIMIT':2,
    'DISSOLVE':False,
    'OUTPUT':'TEMPORARY_OUTPUT'
})['OUTPUT']
QgsProject.instance().addMapLayer(communes_buffered, False)

communesAOI_list = []
commune_zoneStats_list = []

for f in communes_buffered.getFeatures():

    communes_buffered.select(f.id())
    feature_Field_id = str(communes_buffered.selectedFeatures()[0]['id'])
    
    print(feature_Field_id)
    startTimestamp = int(datetime.datetime.now().timestamp())
    
    communes_AOI = processing.run("native:clip", {
        'INPUT':AOI_diff_water_roads_rails_Layer,
        'OVERLAY':QgsProcessingFeatureSourceDefinition(
            communes_buffered.source(),
            selectedFeaturesOnly=True,
            featureLimit=-1,
            flags=QgsProcessingFeatureSourceDefinition.FlagCreateIndividualOutputPerInputFeature,
            geometryCheck=QgsFeatureRequest.GeometryAbortOnInvalid
        ),
        'OUTPUT':'TEMPORARY_OUTPUT'
    })['OUTPUT']
    communesAOI_list.append(communes_AOI)
    QgsProject.instance().addMapLayer(communesAOI_list[-1], True)
    
    clipNDMI = processing.run("gdal:cliprasterbymasklayer", {
        'INPUT':pathNDMI,
        'MASK':communes_AOI,
        'SOURCE_CRS':None,
        'TARGET_CRS':None,
        'TARGET_EXTENT':None,
        'NODATA':-9999,
        'ALPHA_BAND':False,
        'CROP_TO_CUTLINE':True,
        'KEEP_RESOLUTION':False,
        'SET_RESOLUTION':False,
        'X_RESOLUTION':None,
        'Y_RESOLUTION':None,
        'MULTITHREADING':False,
        'OPTIONS':'',
        'DATA_TYPE':0,
        'EXTRA':'',
        'OUTPUT':pathOutNDMI+feature_Field_id+'.tif'
    })['OUTPUT']
    raster_layer_clipNDMI = QgsRasterLayer(clipNDMI, 'clipNDMI')
    QgsProject.instance().addMapLayer(raster_layer_clipNDMI, True)
    
    clipNDVI = processing.run("gdal:cliprasterbymasklayer", {
        'INPUT':pathNDVI,
        'MASK':communes_AOI,
        'SOURCE_CRS':None,
        'TARGET_CRS':None,
        'TARGET_EXTENT':None,
        'NODATA':-9999,
        'ALPHA_BAND':False,
        'CROP_TO_CUTLINE':True,
        'KEEP_RESOLUTION':False,
        'SET_RESOLUTION':False,
        'X_RESOLUTION':None,
        'Y_RESOLUTION':None,
        'MULTITHREADING':False,
        'OPTIONS':'',
        'DATA_TYPE':0,
        'EXTRA':'',
        'OUTPUT':pathOutNDVI+feature_Field_id+'.tif'
    })['OUTPUT']
    raster_layer_clipNDVI = QgsRasterLayer(clipNDVI, 'clipNDVI')
    QgsProject.instance().addMapLayer(raster_layer_clipNDVI, True)
    
    expression = '"id" = {}'.format(f['id'])
    communesLayer.selectByExpression(expression)
    
    commune_zoneStatsNDMI = processing.run("native:zonalstatisticsfb", {
        'INPUT':QgsProcessingFeatureSourceDefinition(
            communesLayer.source(),
            selectedFeaturesOnly=True,
            featureLimit=-1,
            flags=QgsProcessingFeatureSourceDefinition.FlagCreateIndividualOutputPerInputFeature,
            geometryCheck=QgsFeatureRequest.GeometryAbortOnInvalid
        ),
        'INPUT_RASTER':raster_layer_clipNDMI,
        'RASTER_BAND':1,
        'COLUMN_PREFIX':'NDMI_',
        'STATISTICS':[0,1,2],
        'OUTPUT':'TEMPORARY_OUTPUT'
    })['OUTPUT']

    QgsProject.instance().addMapLayer(commune_zoneStatsNDMI, False)
    
    commune_zoneStatsNDVI = processing.run("native:zonalstatisticsfb", {
        'INPUT':QgsProcessingFeatureSourceDefinition(
            commune_zoneStatsNDMI.source(),
            selectedFeaturesOnly=False,
            featureLimit=-1,
            flags=QgsProcessingFeatureSourceDefinition.FlagCreateIndividualOutputPerInputFeature,
            geometryCheck=QgsFeatureRequest.GeometryAbortOnInvalid
        ),
        'INPUT_RASTER':raster_layer_clipNDVI,
        'RASTER_BAND':1,
        'COLUMN_PREFIX':'NDVI_',
        'STATISTICS':[0,1,2],
        'OUTPUT':'TEMPORARY_OUTPUT'
    })['OUTPUT']
    commune_zoneStats_list.append(commune_zoneStatsNDVI)
    QgsProject.instance().addMapLayer(commune_zoneStats_list[-1], False)
    
    endTimestamp = int(datetime.datetime.now().timestamp())
    
    communes_buffered.removeSelection()
    QgsProject.instance().removeMapLayer(communesAOI_list[-1])
    QgsProject.instance().removeMapLayer(raster_layer_clipNDMI)
    QgsProject.instance().removeMapLayer(raster_layer_clipNDVI)
    
    print(endTimestamp - startTimestamp)
    del clipNDMI
    del clipNDVI
    del raster_layer_clipNDMI
    del raster_layer_clipNDVI
    del commune_zoneStatsNDMI
    del commune_zoneStatsNDVI

final = processing.run("native:mergevectorlayers", {
    'LAYERS':commune_zoneStats_list,
    'CRS':QgsCoordinateReferenceSystem('EPSG:32629'),
    'OUTPUT':pathOutFinal+fileOutputName
})['OUTPUT']
finalLayer = QgsVectorLayer(final+'|layername='+fileOutputName[:-5], fileOutputName[:-5], "ogr")
QgsProject.instance().addMapLayer(finalLayer)

subject = 'zar3i - iterateOverCommunes - fim de processo (teste servidor) - {}'.format(varAux)
body = '''
O processo de zonal stats das comunas {} acabou.
O resultado foi guardado no ficheiro {}
'''.format(varAux, fileOutputName)

#sendNotificationMail(subject, body)