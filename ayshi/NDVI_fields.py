import os
# fields pngs
def TIF2colorPNG(listImgs, colorTable, pathOut):
    
    redNDVI = []
    greenNDVI = []
    blueNDVI = []

    for k in colorTable.keys():
        redNDVI+=[colorTable[k]['minValue'], colorTable[k]['maxValue'], colorTable[k]['R']]
        greenNDVI+=[colorTable[k]['minValue'], colorTable[k]['maxValue'], colorTable[k]['G']]
        blueNDVI+=[colorTable[k]['minValue'], colorTable[k]['maxValue'], colorTable[k]['B']]

    for img in listImgs:

        global reclassifyR 
        reclassifyR = processing.run("native:reclassifybytable", {
            'INPUT_RASTER':img.source(),
            'RASTER_BAND':1,
            'TABLE':redNDVI,
            'NO_DATA':-9999,
            'RANGE_BOUNDARIES':1,
            'NODATA_FOR_MISSING':False,
            'DATA_TYPE':1,
            'OUTPUT':'TEMPORARY_OUTPUT'
        })['OUTPUT']
        raster_layer_reclassifyR = QgsRasterLayer(reclassifyR, 'ndviRed')
        #QgsProject.instance().addMapLayer(raster_layer_reclassifyR, True)
        
        global reclassifyG
        reclassifyG = processing.run("native:reclassifybytable", {
            'INPUT_RASTER':img.source(),
            'RASTER_BAND':1,
            'TABLE':greenNDVI,
            'NO_DATA':-9999,
            'RANGE_BOUNDARIES':1,
            'NODATA_FOR_MISSING':False,
            'DATA_TYPE':1,
            'OUTPUT':'TEMPORARY_OUTPUT'
        })['OUTPUT']
        raster_layer_reclassifyG = QgsRasterLayer(reclassifyG, 'ndviGreen')
        #QgsProject.instance().addMapLayer(raster_layer_reclassifyG, True)
        
        global reclassifyB 
        reclassifyB = processing.run("native:reclassifybytable", {
            'INPUT_RASTER':img.source(),
            'RASTER_BAND':1,
            'TABLE':blueNDVI,
            'NO_DATA':-9999,
            'RANGE_BOUNDARIES':1,
            'NODATA_FOR_MISSING':False,
            'DATA_TYPE':1,
            'OUTPUT':'TEMPORARY_OUTPUT'
        })['OUTPUT']
        raster_layer_reclassifyB = QgsRasterLayer(reclassifyB, 'ndviBlue')
        #QgsProject.instance().addMapLayer(raster_layer_reclassifyB, True)

        merged = processing.run("gdal:merge", {
            'INPUT':[reclassifyR, reclassifyG, reclassifyB],
            'PCT':False,
            'SEPARATE':True,
            'NODATA_INPUT':-9999,
            'NODATA_OUTPUT':-9999,
            'OPTIONS':'',
            'EXTRA':'',
            'DATA_TYPE':0,
            'OUTPUT':'TEMPORARY_OUTPUT'
        })['OUTPUT']
        raster_layer_merge = QgsRasterLayer(merged, 'merged')
        #QgsProject.instance().addMapLayer(raster_layer_merge, True)
        
        toPNG = processing.run("gdal:translate", {
            'INPUT':merged,
            'TARGET_CRS':None,
            'NODATA':None,
            'COPY_SUBDATASETS':False,
            'OPTIONS':'',
            'EXTRA':'',
            'DATA_TYPE':1,
            'OUTPUT':pathOut+img.name()+'.png'
        })['OUTPUT']
        raster_layer_toPNG = QgsRasterLayer(toPNG, 'final')
        #QgsProject.instance().addMapLayer(raster_layer_toPNG, True)
        #break


path_output = 'D:/___DEEPFACES_SERVER/zar3i/zar3i_site/202403b/4_communesPNG/Fields_PNGs_direct_seeding/'
path_NDVI = 'D:/___DEEPFACES_SERVER/zar3i/zar3i_site/202403b/2_merge/NDVI.tif'

raster_layer_NDVI = QgsRasterLayer(path_NDVI, 'ndvi')
fieldsLayer = QgsProject.instance().mapLayersByName('agriculture_field')[0]
communeLayer = QgsProject.instance().mapLayersByName('agriculture_commune')[0]

fieldsLayer_fixed = processing.run("native:fixgeometries", {
    'INPUT':fieldsLayer,
    'METHOD':1,
    'OUTPUT':'TEMPORARY_OUTPUT'
})['OUTPUT']

fieldsLayer_reprojected = processing.run("native:reprojectlayer", {
    'INPUT':fieldsLayer_fixed,
    'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:32629'),
    'OPERATION':'+proj=pipeline +step +proj=unitconvert +xy_in=deg +xy_out=rad +step +proj=utm +zone=29 +ellps=WGS84',
    'OUTPUT':'TEMPORARY_OUTPUT'
})['OUTPUT']
QgsProject.instance().addMapLayer(fieldsLayer_reprojected, True)
fieldsLayer_reprojected_dissolved = processing.run("native:dissolve", {
    'INPUT':fieldsLayer_reprojected,
    'FIELD':[],
    'SEPARATE_DISJOINT':False,
    'OUTPUT':'TEMPORARY_OUTPUT'
})['OUTPUT']
QgsProject.instance().addMapLayer(fieldsLayer_reprojected_dissolved, True)

processing.run("native:selectbylocation", {
    'INPUT':communeLayer,
    'PREDICATE':[0],
    'INTERSECT':fieldsLayer_reprojected_dissolved,
    'METHOD':0
})

communes = communeLayer.selectedFeatures()
listImgs = []

#for commune in communes:
#    communeLayer.selectByExpression('"id" = ' + str(commune['id']))
#    
#    processing.run("native:selectbylocation", {
#        'INPUT':fieldsLayer_reprojected,
#        'PREDICATE':[0],
#        'INTERSECT':QgsProcessingFeatureSourceDefinition(
#            communeLayer.source(),
#            selectedFeaturesOnly=True,
#            featureLimit=-1,
#            geometryCheck=QgsFeatureRequest.GeometryAbortOnInvalid
#        ),
#        'METHOD':0
#    })
fields = fieldsLayer_reprojected.getFeatures()
for field in fields:
    fieldsLayer_reprojected.selectByExpression('"id" = ' + str(field['id']))
    NDVI_clip_commune = processing.run("gdal:cliprasterbymasklayer", {
        'INPUT':raster_layer_NDVI.source(),
        'MASK':QgsProcessingFeatureSourceDefinition(
            fieldsLayer_reprojected.source(),
            selectedFeaturesOnly=True,
            featureLimit=-1,
            geometryCheck=QgsFeatureRequest.GeometryAbortOnInvalid
        ),
        'SOURCE_CRS':None,
        'TARGET_CRS':None,
        'TARGET_EXTENT':None,
        'NODATA':None,
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
        'OUTPUT':path_output + 'commune_.tif'
    })['OUTPUT']
    raster_layer_NDVI_commune = QgsRasterLayer(NDVI_clip_commune, 'ndvi_commune')
    
#        NDVI_clip_fields = processing.run("gdal:cliprasterbymasklayer", {
#            'INPUT':raster_layer_NDVI_commune.source(),
#    #        'MASK':QgsProcessingFeatureSourceDefinition(
#    #            fieldsLayer_reprojected.source(),
#    #            selectedFeaturesOnly=True,
#    #            featureLimit=-1,
#    #            geometryCheck=QgsFeatureRequest.GeometryAbortOnInvalid
#    #        ),
#            'MASK': fieldsLayer_reprojected_dissolved_selected,
#            'SOURCE_CRS':None,
#            'TARGET_CRS':None,
#            'TARGET_EXTENT':None,
#            'NODATA':None,
#            'ALPHA_BAND':False,
#            'CROP_TO_CUTLINE':True,
#            'KEEP_RESOLUTION':False,
#            'SET_RESOLUTION':False,
#            'X_RESOLUTION':None,
#            'Y_RESOLUTION':None,
#            'MULTITHREADING':False,
#            'OPTIONS':'',
#            'DATA_TYPE':0,
#            'EXTRA':'',
#            'OUTPUT':path_output + 'field_.tif'
#        })['OUTPUT']
#        raster_layer_NDVI_fields = QgsRasterLayer(NDVI_clip_fields, 'ndvi_field')
    
    NDVI_clip_fields_int16 = processing.run("gdal:rastercalculator", {
        'INPUT_A':raster_layer_NDVI_commune.source(),
        'BAND_A':1,
        'INPUT_B':None,
        'BAND_B':None,
        'INPUT_C':None,
        'BAND_C':None,
        'INPUT_D':None,
        'BAND_D':None,
        'INPUT_E':None,
        'BAND_E':None,
        'INPUT_F':None,
        'BAND_F':None,
        'FORMULA':'A*100',
        'NO_DATA':0,
        'PROJWIN':None,
        'RTYPE':1,
        'OPTIONS':'',
        'EXTRA':'',
        'OUTPUT':path_output + 'id_' + str(field['id']) + '.tif'
    })['OUTPUT']
    raster_layer_NDVIint16 = QgsRasterLayer(NDVI_clip_fields_int16,'id_' + str(field['id']))
    
    extent = raster_layer_NDVIint16.extent()
    provider = raster_layer_NDVIint16.dataProvider()
    stats = provider.bandStatistics(1, QgsRasterBandStats.All, extent, 0)
    min_ = stats.minimumValue
    max_ = stats.maximumValue
    interval = (max_ - min_)
    colorTableNDVI = {
        0:{'minValue': min, 'maxValue': min_+interval/10, 'R':165, 'G':  1, 'B': 38},
        1:{'minValue':  min_+interval/10, 'maxValue': min_+(2*interval)/10, 'R':215, 'G': 48, 'B': 39},
        2:{'minValue':  min_+(2*interval)/10, 'maxValue': min_+(3*interval)/10, 'R':253, 'G':174, 'B': 97},
        3:{'minValue':  min_+(3*interval)/10, 'maxValue': min_+(4*interval)/10, 'R':254, 'G':224, 'B':139},
        4:{'minValue':  min_+(4*interval)/10, 'maxValue': min_+(5*interval)/10, 'R':255, 'G':255, 'B':191},
        5:{'minValue':  min_+(5*interval)/10, 'maxValue': min_+(6*interval)/10, 'R':217, 'G':239, 'B':139},
        6:{'minValue':  min_+(6*interval)/10, 'maxValue': min_+(7*interval)/10, 'R':166, 'G':217, 'B':106},
        7:{'minValue':  min_+(7*interval)/10, 'maxValue': min_+(8*interval)/10, 'R':102, 'G':189, 'B': 99},
        8:{'minValue':  min_+(8*interval)/10, 'maxValue': min_+(9*interval)/10, 'R': 26, 'G':152, 'B': 80},
        9:{'minValue':  min_+(9*interval)/10, 'maxValue':max_+1, 'R': 26, 'G':150, 'B': 65}
    }
    TIF2colorPNG([raster_layer_NDVIint16], colorTableNDVI, path_output)
    del raster_layer_NDVI_commune
    del raster_layer_NDVIint16

#del raster_layer_NDVI_fields
#del listImgs
for filename in os.listdir(path_output):
    print(filename)
    if '.tif' in filename:
        file_path = os.path.join(path_output, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    else:
        pass