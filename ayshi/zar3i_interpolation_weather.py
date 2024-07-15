import psycopg2
exec(open('D:/___DEEPFACES_SERVER/zar3i/scripts/0_greenWorldPyQgis.py').read())

layerCommunes = QgsProject.instance().mapLayersByName('agriculture_commune')[0]
layer_stations = QgsProject.instance().mapLayersByName('weather_2015_2022')[0]
layer_stations_2023 = QgsProject.instance().mapLayersByName('weather_2023')[0]

#years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
year = 2023
months = list(range(1,13))

#for month in months:
#    deleteTemporaryLayers()
#    expression = '"month" = {}'.format(month)
#    print(month)
#    layer_stations.selectByExpression(expression)
#
#    stationsLayerReproj = processing.run("native:reprojectlayer", {
#        'INPUT':QgsProcessingFeatureSourceDefinition(
#            layer_stations.source(),
#            selectedFeaturesOnly=True,
#            featureLimit=-1,
#            geometryCheck=QgsFeatureRequest.GeometryAbortOnInvalid
#        ),
#        'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:32629'),
#        #'OPERATION':'+proj=pipeline +step +proj=unitconvert +xy_in=deg +xy_out=rad +step +proj=utm +zone=30 +ellps=WGS84',
#        'OUTPUT':'TEMPORARY_OUTPUT'
#    })['OUTPUT']
#
#    QgsProject.instance().addMapLayer(stationsLayerReproj, True)
#    
#    extent = '288349.048400000,1162488.579400000,3148754.973300000,3958043.949800000 [EPSG:32629]'
#
#    tinMax = processing.run("qgis:tininterpolation", {
#        'INTERPOLATION_DATA':stationsLayerReproj.source()+'::~::0::~::4::~::0', ## str auxiliar retirada dos logs/parametros na janela da op no QGIS
#        'METHOD':1,
#        'EXTENT':extent,
#        'PIXEL_SIZE':1000,
#        'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
#    })['OUTPUT']
#    raster_layer_tinMax = QgsRasterLayer(tinMax, 'tinMax')
#    QgsProject.instance().addMapLayer(raster_layer_tinMax)
#
#    tinMin = processing.run("qgis:tininterpolation", {
#        'INTERPOLATION_DATA':stationsLayerReproj.source()+'::~::0::~::5::~::0', ## str auxiliar retirada dos logs/parametros na janela da op no QGIS
#        'METHOD':1,
#        'EXTENT':extent,
#        'PIXEL_SIZE':1000,
#        'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
#    })['OUTPUT']
#    raster_layer_tinMin = QgsRasterLayer(tinMin, 'tinMin')
#    QgsProject.instance().addMapLayer(raster_layer_tinMin)
#    
#    tinAvg = processing.run("qgis:tininterpolation", {
#        'INTERPOLATION_DATA':stationsLayerReproj.source()+'::~::0::~::3::~::0', ## str auxiliar retirada dos logs/parametros na janela da op no QGIS
#        'METHOD':0,
#        'EXTENT':extent,
#        'PIXEL_SIZE':1000,
#        'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
#    })['OUTPUT']
#    raster_layer_tinAvg = QgsRasterLayer(tinAvg, 'tinAvg')
#    QgsProject.instance().addMapLayer(raster_layer_tinAvg)
#    
#    tinPrecipMax = processing.run("qgis:tininterpolation", {
#        'INTERPOLATION_DATA':stationsLayerReproj.source()+'::~::0::~::12::~::0', ## str auxiliar retirada dos logs/parametros na janela da op no QGIS
#        'METHOD':0,
#        'EXTENT':extent,
#        'PIXEL_SIZE':1000,
#        'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
#    })['OUTPUT']
#    raster_layer_tinPrecipMax = QgsRasterLayer(tinPrecipMax, 'tinPrecipMax')
#    QgsProject.instance().addMapLayer(raster_layer_tinPrecipMax)
#    
#    tinPrecipSum = processing.run("qgis:tininterpolation", {
#        'INTERPOLATION_DATA':stationsLayerReproj.source()+'::~::0::~::13::~::0', ## str auxiliar retirada dos logs/parametros na janela da op no QGIS
#        'METHOD':0,
#        'EXTENT':extent,
#        'PIXEL_SIZE':1000,
#        'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
#    })['OUTPUT']
#    raster_layer_tinPrecipSum = QgsRasterLayer(tinPrecipSum, 'tinPrecipSum')
#    QgsProject.instance().addMapLayer(raster_layer_tinPrecipSum)
#    
#    ### Zonal Min
#
#    zonalStatsMin = processing.run("native:zonalstatisticsfb", {
#        'INPUT':layerCommunes,
#        'INPUT_RASTER':raster_layer_tinMin,
#        'RASTER_BAND':1,
#        'COLUMN_PREFIX':'_Min_',
#        'STATISTICS':[2],
#        'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
#    })['OUTPUT']
#    #QgsProject.instance().addMapLayer(zonalStatsMin)
#    zonalStatsMin.selectAll()
#
#    clone_zonalStatsMin = processing.run("native:saveselectedfeatures", {'INPUT': zonalStatsMin, 'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT})['OUTPUT']
#
#    zonalStatsMin.removeSelection()
#
#    QgsProject.instance().addMapLayer(clone_zonalStatsMin)
#    clone_zonalStatsMin.setName('clone_zonalStatsMin')
#    clone_zonalStatsMin.setSubsetString("_Min_mean is not NULL")
#
#    zonalStatsMin.setSubsetString("_Min_mean is NULL")
#
#    zonalStatsMin.selectAll()
#    zonalStatsMin.startEditing()
#
#    expression = QgsExpression("array_to_string(overlay_nearest("+"'clone_zonalStatsMin',"+'"_Min_mean"))')
#
#    for f in zonalStatsMin.selectedFeatures():
#        context = QgsExpressionContext()
#        context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(zonalStatsMin))
#        context.setFeature(f)
#        f['_Min_mean'] = expression.evaluate(context)
#        zonalStatsMin.updateFeature(f)
#    zonalStatsMin.commitChanges()
#    zonalStatsMin.setSubsetString('')
#
#    #### Zonal Max
#    ## zonal statistics Max temp
#    zonalStatsMax = processing.run("native:zonalstatisticsfb", {
#        'INPUT':zonalStatsMin,
#        'INPUT_RASTER':raster_layer_tinMax,
#        'RASTER_BAND':1,
#        'COLUMN_PREFIX':'_Max_',
#        'STATISTICS':[2],
#        'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
#    })['OUTPUT']
#    #QgsProject.instance().addMapLayer(zonalStatsMax)
#    zonalStatsMax.selectAll()
#
#    ## clone zonalStats temp (auxiliar para calcular os NULLs com base na feature mais próxima)
#    clone_zonalStatsMax = processing.run("native:saveselectedfeatures", {'INPUT': zonalStatsMax, 'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT})['OUTPUT']
#
#    zonalStatsMax.removeSelection()
#
#    QgsProject.instance().addMapLayer(clone_zonalStatsMax)
#    clone_zonalStatsMax.setName('clone_zonalStatsMax')
#    clone_zonalStatsMax.setSubsetString("_Max_mean is not NULL")
#
#    zonalStatsMax.setSubsetString("_Max_mean is NULL")
#
#    zonalStatsMax.selectAll()
#    zonalStatsMax.startEditing()
#
#    expression = QgsExpression("array_to_string(overlay_nearest("+"'clone_zonalStatsMax',"+'"_Max_mean"))')
#
#    for f in zonalStatsMax.selectedFeatures():
#        context = QgsExpressionContext()
#        context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(zonalStatsMax))
#        context.setFeature(f)
#        f['_Max_mean'] = expression.evaluate(context)
#        zonalStatsMax.updateFeature(f)
#    zonalStatsMax.commitChanges()
#    zonalStatsMax.setSubsetString('')
#
#    #### Zonal Avg
#    ## zonal statistics Max temp
#    zonalStatsAvg = processing.run("native:zonalstatisticsfb", {
#        'INPUT':zonalStatsMax,
#        'INPUT_RASTER':raster_layer_tinAvg,
#        'RASTER_BAND':1,
#        'COLUMN_PREFIX':'_Avg_',
#        'STATISTICS':[2],
#        'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
#    })['OUTPUT']
#    #QgsProject.instance().addMapLayer(zonalStatsMax)
#    zonalStatsAvg.selectAll()
#
#    ## clone zonalStats temp (auxiliar para calcular os NULLs com base na feature mais próxima)
#    clone_zonalStatsAvg = processing.run("native:saveselectedfeatures", {'INPUT': zonalStatsAvg, 'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT})['OUTPUT']
#
#    zonalStatsAvg.removeSelection()
#
#    QgsProject.instance().addMapLayer(clone_zonalStatsAvg)
#    clone_zonalStatsAvg.setName('clone_zonalStatsAvg')
#    clone_zonalStatsAvg.setSubsetString("_Avg_mean is not NULL")
#
#    zonalStatsAvg.setSubsetString("_Avg_mean is NULL")
#
#    zonalStatsAvg.selectAll()
#    zonalStatsAvg.startEditing()
#
#    expression = QgsExpression("array_to_string(overlay_nearest("+"'clone_zonalStatsAvg',"+'"_Avg_mean"))')
#
#    for f in zonalStatsAvg.selectedFeatures():
#        context = QgsExpressionContext()
#        context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(zonalStatsAvg))
#        context.setFeature(f)
#        f['_Avg_mean'] = expression.evaluate(context)
#        zonalStatsAvg.updateFeature(f)
#    zonalStatsAvg.commitChanges()
#    zonalStatsAvg.setSubsetString('')
#
#    #### Zonal Precip
#    ## zonal statistics Max temp
#    zonalStatsPrecipMax = processing.run("native:zonalstatisticsfb", {
#        'INPUT':zonalStatsAvg,
#        'INPUT_RASTER':raster_layer_tinPrecipMax,
#        'RASTER_BAND':1,
#        'COLUMN_PREFIX':'_PrecipMax_',
#        'STATISTICS':[2],
#        'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
#    })['OUTPUT']
#    QgsProject.instance().addMapLayer(zonalStatsPrecipMax)
#    zonalStatsPrecipMax.selectAll()
#
#    ## clone zonalStats temp (auxiliar para calcular os NULLs com base na feature mais próxima)
#    clone_zonalStatsPrecipMax = processing.run("native:saveselectedfeatures", {'INPUT': zonalStatsPrecipMax, 'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT})['OUTPUT']
#
#    zonalStatsPrecipMax.removeSelection()
#
#    QgsProject.instance().addMapLayer(clone_zonalStatsPrecipMax)
#    clone_zonalStatsPrecipMax.setName('clone_zonalStatsPrecipMax')
#    clone_zonalStatsPrecipMax.setSubsetString("_PrecipMax_mean is not NULL")
#
#    zonalStatsPrecipMax.setSubsetString("_PrecipMax_mean is NULL")
#
#    zonalStatsPrecipMax.selectAll()
#    zonalStatsPrecipMax.startEditing()
#
#    expression = QgsExpression("array_to_string(overlay_nearest("+"'clone_zonalStatsPrecipMax',"+'"_PrecipMax_mean"))')
#
#    for f in zonalStatsPrecipMax.selectedFeatures():
#        context = QgsExpressionContext()
#        context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(zonalStatsPrecipMax))
#        context.setFeature(f)
#        f['_PrecipMax_mean'] = expression.evaluate(context)
#        zonalStatsPrecipMax.updateFeature(f)
#    zonalStatsPrecipMax.commitChanges()
#    zonalStatsPrecipMax.setSubsetString('')
#    
#    #### Zonal Precip
#    ## zonal statistics Sum temp
#    zonalStatsPrecipSum = processing.run("native:zonalstatisticsfb", {
#        'INPUT':zonalStatsPrecipMax,
#        'INPUT_RASTER':raster_layer_tinPrecipSum,
#        'RASTER_BAND':1,
#        'COLUMN_PREFIX':'_PrecipSum_',
#        'STATISTICS':[2],
#        'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
#    })['OUTPUT']
#    QgsProject.instance().addMapLayer(zonalStatsPrecipSum)
#    zonalStatsPrecipSum.selectAll()
#
#    ## clone zonalStats temp (auxiliar para calcular os NULLs com base na feature mais próxima)
#    clone_zonalStatsPrecipSum = processing.run("native:saveselectedfeatures", {'INPUT': zonalStatsPrecipSum, 'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT})['OUTPUT']
#
#    zonalStatsPrecipSum.removeSelection()
#
#    QgsProject.instance().addMapLayer(clone_zonalStatsPrecipSum)
#    clone_zonalStatsPrecipSum.setName('clone_zonalStatsPrecipSum')
#    clone_zonalStatsPrecipSum.setSubsetString("_PrecipSum_mean is not NULL")
#
#    zonalStatsPrecipSum.setSubsetString("_PrecipSum_mean is NULL")
#
#    zonalStatsPrecipSum.selectAll()
#    zonalStatsPrecipSum.startEditing()
#
#    expression = QgsExpression("array_to_string(overlay_nearest("+"'clone_zonalStatsPrecipSum',"+'"_PrecipSum_mean"))')
#
#    for f in zonalStatsPrecipSum.selectedFeatures():
#        context = QgsExpressionContext()
#        context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(zonalStatsPrecipSum))
#        context.setFeature(f)
#        f['_PrecipSum_mean'] = expression.evaluate(context)
#        zonalStatsPrecipSum.updateFeature(f)
#    zonalStatsPrecipSum.commitChanges()
#    zonalStatsPrecipSum.setSubsetString('')
#
#    QgsProject.instance().removeMapLayer(clone_zonalStatsMin)
#    QgsProject.instance().removeMapLayer(clone_zonalStatsMax)
#    QgsProject.instance().removeMapLayer(clone_zonalStatsAvg)
#    QgsProject.instance().removeMapLayer(clone_zonalStatsPrecipMax)
#    QgsProject.instance().removeMapLayer(clone_zonalStatsPrecipSum)
#    
#    zonalStatsPrecipSum.selectAll()
#
#    #dateToday_format = date[6:8] + '/' + date[4:6] + '/' + date[:4]
#    conn = psycopg2.connect(
#       database="ayishi", user='developer', password='ObuEm8Ap', host='165.227.135.116', port= '5432'
#    )
#    conn.autocommit = True
#    cursor = conn.cursor()
#
#    for feat in zonalStatsPrecipSum.selectedFeatures():
#        command1 = "INSERT INTO zar3i.agriculture_weather VALUES (default,{},{},{},{},{},{},default,default,{},{})".format(month, feat['_Avg_mean'], feat['_Min_mean'], feat['_Max_mean'], feat['_PrecipSum_mean'], feat['_PrecipMax_mean'], feat['id'], year)
#        command2 = "INSERT INTO icarda.agriculture_weather VALUES (default,{},{},{},{},{},{},default,default,{},{})".format(month, feat['_Avg_mean'], feat['_Min_mean'], feat['_Max_mean'], feat['_PrecipSum_mean'], feat['_PrecipMax_mean'], feat['id'], year)
#        cursor.execute(command1)
#        cursor.execute(command2)
#        conn.commit()
#    conn.close()
#    
#    QgsProject.instance().removeMapLayer(stationsLayerReproj)
#    QgsProject.instance().removeMapLayer(zonalStatsMin)
#    QgsProject.instance().removeMapLayer(zonalStatsMax)
#    QgsProject.instance().removeMapLayer(zonalStatsAvg)
#    QgsProject.instance().removeMapLayer(zonalStatsPrecipMax)
#    QgsProject.instance().removeMapLayer(zonalStatsPrecipSum)
#
#    QgsProject.instance().removeMapLayer(raster_layer_tinMax)
#    QgsProject.instance().removeMapLayer(raster_layer_tinMin)
#    QgsProject.instance().removeMapLayer(raster_layer_tinAvg)
#    QgsProject.instance().removeMapLayer(raster_layer_tinPrecipMax)
#    QgsProject.instance().removeMapLayer(raster_layer_tinPrecipSum)
#
#    del zonalStatsPrecipSum
#    del zonalStatsMin
#    del zonalStatsMax
#    del stationsLayerReproj
#    del zonalStatsPrecipMax
#    del zonalStatsAvg

for month in months:
    deleteTemporaryLayers()
    expression = '"month" = {}'.format(month)
    
    layer_stations_2023.selectByExpression(expression)

    stationsLayerReproj = processing.run("native:reprojectlayer", {
        'INPUT':QgsProcessingFeatureSourceDefinition(
            layer_stations_2023.source(),
            selectedFeaturesOnly=True,
            featureLimit=-1,
            geometryCheck=QgsFeatureRequest.GeometryAbortOnInvalid
        ),
        'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:32629'),
        #'OPERATION':'+proj=pipeline +step +proj=unitconvert +xy_in=deg +xy_out=rad +step +proj=utm +zone=30 +ellps=WGS84',
        'OUTPUT':'TEMPORARY_OUTPUT'
    })['OUTPUT']

    QgsProject.instance().addMapLayer(stationsLayerReproj, True)
    
    extent = '288349.050000000,1162488.583700000,3148755.000000000,3958043.982000000 [EPSG:32629]'

    tinMax = processing.run("qgis:tininterpolation", {
        'INTERPOLATION_DATA':stationsLayerReproj.source()+'::~::0::~::4::~::0', ## str auxiliar retirada dos logs/parametros na janela da op no QGIS
        'METHOD':1,
        'EXTENT':extent,
        'PIXEL_SIZE':1000,
        'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
    })['OUTPUT']
    raster_layer_tinMax = QgsRasterLayer(tinMax, 'tinMax')
    QgsProject.instance().addMapLayer(raster_layer_tinMax)

    tinMin = processing.run("qgis:tininterpolation", {
        'INTERPOLATION_DATA':stationsLayerReproj.source()+'::~::0::~::5::~::0', ## str auxiliar retirada dos logs/parametros na janela da op no QGIS
        'METHOD':1,
        'EXTENT':extent,
        'PIXEL_SIZE':1000,
        'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
    })['OUTPUT']
    raster_layer_tinMin = QgsRasterLayer(tinMin, 'tinMin')
    QgsProject.instance().addMapLayer(raster_layer_tinMin)
    
    tinAvg = processing.run("qgis:tininterpolation", {
        'INTERPOLATION_DATA':stationsLayerReproj.source()+'::~::0::~::3::~::0', ## str auxiliar retirada dos logs/parametros na janela da op no QGIS
        'METHOD':0,
        'EXTENT':extent,
        'PIXEL_SIZE':1000,
        'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
    })['OUTPUT']
    raster_layer_tinAvg = QgsRasterLayer(tinAvg, 'tinAvg')
    QgsProject.instance().addMapLayer(raster_layer_tinAvg)
    
    tinPrecipMax = processing.run("qgis:tininterpolation", {
        'INTERPOLATION_DATA':stationsLayerReproj.source()+'::~::0::~::12::~::0', ## str auxiliar retirada dos logs/parametros na janela da op no QGIS
        'METHOD':0,
        'EXTENT':extent,
        'PIXEL_SIZE':1000,
        'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
    })['OUTPUT']
    raster_layer_tinPrecipMax = QgsRasterLayer(tinPrecipMax, 'tinPrecipMax')
    QgsProject.instance().addMapLayer(raster_layer_tinPrecipMax)
    
    tinPrecipSum = processing.run("qgis:tininterpolation", {
        'INTERPOLATION_DATA':stationsLayerReproj.source()+'::~::0::~::13::~::0', ## str auxiliar retirada dos logs/parametros na janela da op no QGIS
        'METHOD':0,
        'EXTENT':extent,
        'PIXEL_SIZE':1000,
        'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
    })['OUTPUT']
    raster_layer_tinPrecipSum = QgsRasterLayer(tinPrecipSum, 'tinPrecipSum')
    QgsProject.instance().addMapLayer(raster_layer_tinPrecipSum)
    
    ### Zonal Min

    zonalStatsMin = processing.run("native:zonalstatisticsfb", {
        'INPUT':layerCommunes,
        'INPUT_RASTER':raster_layer_tinMin,
        'RASTER_BAND':1,
        'COLUMN_PREFIX':'_Min_',
        'STATISTICS':[2],
        'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
    })['OUTPUT']
    #QgsProject.instance().addMapLayer(zonalStatsMin)
    zonalStatsMin.selectAll()

    clone_zonalStatsMin = processing.run("native:saveselectedfeatures", {'INPUT': zonalStatsMin, 'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT})['OUTPUT']

    zonalStatsMin.removeSelection()

    QgsProject.instance().addMapLayer(clone_zonalStatsMin)
    clone_zonalStatsMin.setName('clone_zonalStatsMin')
    clone_zonalStatsMin.setSubsetString("_Min_mean is not NULL")

    zonalStatsMin.setSubsetString("_Min_mean is NULL")

    zonalStatsMin.selectAll()
    zonalStatsMin.startEditing()

    expression = QgsExpression("array_to_string(overlay_nearest("+"'clone_zonalStatsMin',"+'"_Min_mean"))')

    for f in zonalStatsMin.selectedFeatures():
        context = QgsExpressionContext()
        context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(zonalStatsMin))
        context.setFeature(f)
        f['_Min_mean'] = expression.evaluate(context)
        zonalStatsMin.updateFeature(f)
    zonalStatsMin.commitChanges()
    zonalStatsMin.setSubsetString('')

    #### Zonal Max
    ## zonal statistics Max temp
    zonalStatsMax = processing.run("native:zonalstatisticsfb", {
        'INPUT':zonalStatsMin,
        'INPUT_RASTER':raster_layer_tinMax,
        'RASTER_BAND':1,
        'COLUMN_PREFIX':'_Max_',
        'STATISTICS':[2],
        'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
    })['OUTPUT']
    #QgsProject.instance().addMapLayer(zonalStatsMax)
    zonalStatsMax.selectAll()

    ## clone zonalStats temp (auxiliar para calcular os NULLs com base na feature mais próxima)
    clone_zonalStatsMax = processing.run("native:saveselectedfeatures", {'INPUT': zonalStatsMax, 'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT})['OUTPUT']

    zonalStatsMax.removeSelection()

    QgsProject.instance().addMapLayer(clone_zonalStatsMax)
    clone_zonalStatsMax.setName('clone_zonalStatsMax')
    clone_zonalStatsMax.setSubsetString("_Max_mean is not NULL")

    zonalStatsMax.setSubsetString("_Max_mean is NULL")

    zonalStatsMax.selectAll()
    zonalStatsMax.startEditing()

    expression = QgsExpression("array_to_string(overlay_nearest("+"'clone_zonalStatsMax',"+'"_Max_mean"))')

    for f in zonalStatsMax.selectedFeatures():
        context = QgsExpressionContext()
        context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(zonalStatsMax))
        context.setFeature(f)
        f['_Max_mean'] = expression.evaluate(context)
        zonalStatsMax.updateFeature(f)
    zonalStatsMax.commitChanges()
    zonalStatsMax.setSubsetString('')

    #### Zonal Avg
    ## zonal statistics Max temp
    zonalStatsAvg = processing.run("native:zonalstatisticsfb", {
        'INPUT':zonalStatsMax,
        'INPUT_RASTER':raster_layer_tinAvg,
        'RASTER_BAND':1,
        'COLUMN_PREFIX':'_Avg_',
        'STATISTICS':[2],
        'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
    })['OUTPUT']
    #QgsProject.instance().addMapLayer(zonalStatsMax)
    zonalStatsAvg.selectAll()

    ## clone zonalStats temp (auxiliar para calcular os NULLs com base na feature mais próxima)
    clone_zonalStatsAvg = processing.run("native:saveselectedfeatures", {'INPUT': zonalStatsAvg, 'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT})['OUTPUT']

    zonalStatsAvg.removeSelection()

    QgsProject.instance().addMapLayer(clone_zonalStatsAvg)
    clone_zonalStatsAvg.setName('clone_zonalStatsAvg')
    clone_zonalStatsAvg.setSubsetString("_Avg_mean is not NULL")

    zonalStatsAvg.setSubsetString("_Avg_mean is NULL")

    zonalStatsAvg.selectAll()
    zonalStatsAvg.startEditing()

    expression = QgsExpression("array_to_string(overlay_nearest("+"'clone_zonalStatsAvg',"+'"_Avg_mean"))')

    for f in zonalStatsAvg.selectedFeatures():
        context = QgsExpressionContext()
        context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(zonalStatsAvg))
        context.setFeature(f)
        f['_Avg_mean'] = expression.evaluate(context)
        zonalStatsAvg.updateFeature(f)
    zonalStatsAvg.commitChanges()
    zonalStatsAvg.setSubsetString('')

    #### Zonal Precip
    ## zonal statistics Max temp
    zonalStatsPrecipMax = processing.run("native:zonalstatisticsfb", {
        'INPUT':zonalStatsAvg,
        'INPUT_RASTER':raster_layer_tinPrecipMax,
        'RASTER_BAND':1,
        'COLUMN_PREFIX':'_PrecipMax_',
        'STATISTICS':[2],
        'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
    })['OUTPUT']
    QgsProject.instance().addMapLayer(zonalStatsPrecipMax)
    zonalStatsPrecipMax.selectAll()

    ## clone zonalStats temp (auxiliar para calcular os NULLs com base na feature mais próxima)
    clone_zonalStatsPrecipMax = processing.run("native:saveselectedfeatures", {'INPUT': zonalStatsPrecipMax, 'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT})['OUTPUT']

    zonalStatsPrecipMax.removeSelection()

    QgsProject.instance().addMapLayer(clone_zonalStatsPrecipMax)
    clone_zonalStatsPrecipMax.setName('clone_zonalStatsPrecipMax')
    clone_zonalStatsPrecipMax.setSubsetString("_PrecipMax_mean is not NULL")

    zonalStatsPrecipMax.setSubsetString("_PrecipMax_mean is NULL")

    zonalStatsPrecipMax.selectAll()
    zonalStatsPrecipMax.startEditing()

    expression = QgsExpression("array_to_string(overlay_nearest("+"'clone_zonalStatsPrecipMax',"+'"_PrecipMax_mean"))')

    for f in zonalStatsPrecipMax.selectedFeatures():
        context = QgsExpressionContext()
        context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(zonalStatsPrecipMax))
        context.setFeature(f)
        f['_PrecipMax_mean'] = expression.evaluate(context)
        zonalStatsPrecipMax.updateFeature(f)
    zonalStatsPrecipMax.commitChanges()
    zonalStatsPrecipMax.setSubsetString('')
    
    #### Zonal Precip
    ## zonal statistics Sum temp
    zonalStatsPrecipSum = processing.run("native:zonalstatisticsfb", {
        'INPUT':zonalStatsPrecipMax,
        'INPUT_RASTER':raster_layer_tinPrecipSum,
        'RASTER_BAND':1,
        'COLUMN_PREFIX':'_PrecipSum_',
        'STATISTICS':[2],
        'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
    })['OUTPUT']
    QgsProject.instance().addMapLayer(zonalStatsPrecipSum)
    zonalStatsPrecipSum.selectAll()

    ## clone zonalStats temp (auxiliar para calcular os NULLs com base na feature mais próxima)
    clone_zonalStatsPrecipSum = processing.run("native:saveselectedfeatures", {'INPUT': zonalStatsPrecipSum, 'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT})['OUTPUT']

    zonalStatsPrecipSum.removeSelection()

    QgsProject.instance().addMapLayer(clone_zonalStatsPrecipSum)
    clone_zonalStatsPrecipSum.setName('clone_zonalStatsPrecipSum')
    clone_zonalStatsPrecipSum.setSubsetString("_PrecipSum_mean is not NULL")

    zonalStatsPrecipSum.setSubsetString("_PrecipSum_mean is NULL")

    zonalStatsPrecipSum.selectAll()
    zonalStatsPrecipSum.startEditing()

    expression = QgsExpression("array_to_string(overlay_nearest("+"'clone_zonalStatsPrecipSum',"+'"_PrecipSum_mean"))')

    for f in zonalStatsPrecipSum.selectedFeatures():
        context = QgsExpressionContext()
        context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(zonalStatsPrecipSum))
        context.setFeature(f)
        f['_PrecipSum_mean'] = expression.evaluate(context)
        zonalStatsPrecipSum.updateFeature(f)
    zonalStatsPrecipSum.commitChanges()
    zonalStatsPrecipSum.setSubsetString('')

    QgsProject.instance().removeMapLayer(clone_zonalStatsMin)
    QgsProject.instance().removeMapLayer(clone_zonalStatsMax)
    QgsProject.instance().removeMapLayer(clone_zonalStatsAvg)
    QgsProject.instance().removeMapLayer(clone_zonalStatsPrecipMax)
    QgsProject.instance().removeMapLayer(clone_zonalStatsPrecipSum)
    
    zonalStatsPrecipSum.selectAll()

    #dateToday_format = date[6:8] + '/' + date[4:6] + '/' + date[:4]
    conn = psycopg2.connect(
       database="ayishi", user='developer', password='ObuEm8Ap', host='165.227.135.116', port= '5432'
    )
    conn.autocommit = True
    cursor = conn.cursor()

    for feat in zonalStatsPrecipSum.selectedFeatures():
        command1 = "UPDATE zar3i.agriculture_weather SET temp_avg_current = {}, precip_sum_current = {} WHERE commune_id = {} AND month = {}".format(feat['_Avg_mean'], feat['_PrecipSum_mean'], feat['id'], month)
        command2 = "UPDATE icarda.agriculture_weather SET temp_avg_current = {}, precip_sum_current = {} WHERE commune_id = {} AND month = {}".format(feat['_Avg_mean'], feat['_PrecipSum_mean'], feat['id'], month)
        cursor.execute(command1)
        cursor.execute(command2)
        conn.commit()
    conn.close()
    
    QgsProject.instance().removeMapLayer(stationsLayerReproj)
    QgsProject.instance().removeMapLayer(zonalStatsMin)
    QgsProject.instance().removeMapLayer(zonalStatsMax)
    QgsProject.instance().removeMapLayer(zonalStatsAvg)
    QgsProject.instance().removeMapLayer(zonalStatsPrecipMax)
    QgsProject.instance().removeMapLayer(zonalStatsPrecipSum)

    QgsProject.instance().removeMapLayer(raster_layer_tinMax)
    QgsProject.instance().removeMapLayer(raster_layer_tinMin)
    QgsProject.instance().removeMapLayer(raster_layer_tinAvg)
    QgsProject.instance().removeMapLayer(raster_layer_tinPrecipMax)
    QgsProject.instance().removeMapLayer(raster_layer_tinPrecipSum)

    del zonalStatsPrecipSum
    del zonalStatsMin
    del zonalStatsMax
    del stationsLayerReproj
    del zonalStatsPrecipMax
    del zonalStatsAvg

