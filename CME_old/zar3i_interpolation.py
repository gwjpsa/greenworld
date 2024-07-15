#exec(open('C:/Users/joaos/OneDrive/Ambiente de Trabalho/QGIS_TESTES/scripts finalizados/greenWorldPyQgis.py').read())
import psycopg2

deleteTemporaryLayers()

temp_stations = QgsProject.instance().mapLayersByName('temp_stations')[0]
layerCommunes = QgsProject.instance().mapLayersByName('agriculture_commune')[0]
layerCommunes.setSubsetString(
    '"Code_Region" = {} OR \
    "Code_Region" = {} OR\
    "Code_Region" = {} OR\
    "Code_Region" = {} OR\
    "Code_Region" = {}'.format('\'03.\'', '\'04.\'', '\'05.\'', '\'06.\'','\'07.\'')
)

temp_stations.selectAll()
dates = []
for f in temp_stations.selectedFeatures():
    dates.append(f['DATE'])

uniqueDates, dump = getUniqueAndDuplicated(dates)
#uniqueDates = ['20221209']
newList = []
for d in uniqueDates:
    if int(d[4:]) > 1114:
        newList.append(d)
#for date in uniqueDates: ############################ EDITAR ESTAS LINHAS
for date in newList:
    expression = '"DATE" = {}'.format(date)
    temp_stations.selectByExpression(expression)

    ## inicialização da layer temporária dos pontos iniciais e/ou finais (que são duplicados) de cada troço
    stationsLayer = QgsVectorLayer("Point?crs=epsg:4326", "tempStations", "memory")
    stationsLayer.dataProvider().addAttributes([
        QgsField('maxTemp', QVariant.Double),
        QgsField('minTemp', QVariant.Double),
        QgsField('precip', QVariant.Double),
    ])
    stationsLayer.updateFields()
    stationsLayer.startEditing()

    ## pontos iniciais
    for elem in temp_stations.selectedFeatures():
        feat = QgsFeature()
        feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(elem['LONGITUDE'], elem['LATITUDE'])))
        feat.setAttributes([elem['MAX_TMP'], elem['MIN_TMP'], elem['PRECIP_TOTAL']])
        stationsLayer.addFeature(feat)

    stationsLayer.commitChanges()

    #QgsProject.instance().addMapLayer(stationsLayer, True

    stationsLayerReproj = processing.run("native:reprojectlayer", {
        'INPUT':stationsLayer,
        'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:32629'),
        'OPERATION':'+proj=pipeline +step +proj=unitconvert +xy_in=deg +xy_out=rad +step +proj=utm +zone=29 +ellps=WGS84',
        'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
    })['OUTPUT']

    QgsProject.instance().addMapLayer(stationsLayerReproj, True)

    extent = '288349.050000000,1162488.583700000,3148755.000000000,3958043.982000000 [EPSG:32629]'

    tinMin = processing.run("qgis:tininterpolation", {
        'INTERPOLATION_DATA':stationsLayerReproj.source()+'::~::0::~::1::~::0', ## str auxiliar retirada dos logs/parametros na janela da op no QGIS
        'METHOD':1,
        'EXTENT':extent,
        'PIXEL_SIZE':1000,
        'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
    })['OUTPUT']
    raster_layer_minTemp = QgsRasterLayer(tinMin, 'tinMin')
    #QgsProject.instance().addMapLayer(raster_layer_minTemp)

    tinMax = processing.run("qgis:tininterpolation", {
        'INTERPOLATION_DATA':stationsLayerReproj.source()+'::~::0::~::0::~::0', ## str auxiliar retirada dos logs/parametros na janela da op no QGIS
        'METHOD':1,
        'EXTENT':extent,
        'PIXEL_SIZE':1000,
        'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
    })['OUTPUT']
    raster_layer_maxTemp = QgsRasterLayer(tinMax, 'tinMax')
    #QgsProject.instance().addMapLayer(raster_layer_maxTemp)
    
    tinPrecip = processing.run("qgis:tininterpolation", {
        'INTERPOLATION_DATA':stationsLayerReproj.source()+'::~::0::~::2::~::0', ## str auxiliar retirada dos logs/parametros na janela da op no QGIS
        'METHOD':0,
        'EXTENT':extent,
        'PIXEL_SIZE':1000,
        'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
    })['OUTPUT']
    raster_layer_tinPrecip = QgsRasterLayer(tinPrecip, 'tinPrecip')
    #QgsProject.instance().addMapLayer(raster_layer_tinPrecip)
    
    ### Zonal Min

    zonalStatsMin = processing.run("native:zonalstatisticsfb", {
        'INPUT':layerCommunes,
        'INPUT_RASTER':raster_layer_minTemp,
        'RASTER_BAND':1,
        'COLUMN_PREFIX':'_Min_',
        'STATISTICS':[0,1,2],
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
        'INPUT_RASTER':raster_layer_maxTemp,
        'RASTER_BAND':1,
        'COLUMN_PREFIX':'_Max_',
        'STATISTICS':[0,1,2],
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

    #### Zonal Precip
    ## zonal statistics Max temp
    zonalStatsPrecip = processing.run("native:zonalstatisticsfb", {
        'INPUT':zonalStatsMax,
        'INPUT_RASTER':raster_layer_tinPrecip,
        'RASTER_BAND':1,
        'COLUMN_PREFIX':'_Precip_',
        'STATISTICS':[0,1,2],
        'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
    })['OUTPUT']
    QgsProject.instance().addMapLayer(zonalStatsPrecip)
    zonalStatsPrecip.selectAll()

    ## clone zonalStats temp (auxiliar para calcular os NULLs com base na feature mais próxima)
    clone_zonalStatsPrecip = processing.run("native:saveselectedfeatures", {'INPUT': zonalStatsPrecip, 'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT})['OUTPUT']

    zonalStatsPrecip.removeSelection()

    QgsProject.instance().addMapLayer(clone_zonalStatsPrecip)
    clone_zonalStatsPrecip.setName('clone_zonalStatsPrecip')
    clone_zonalStatsPrecip.setSubsetString("_Precip_mean is not NULL")

    zonalStatsPrecip.setSubsetString("_Precip_mean is NULL")

    zonalStatsPrecip.selectAll()
    zonalStatsPrecip.startEditing()

    expression = QgsExpression("array_to_string(overlay_nearest("+"'clone_zonalStatsPrecip',"+'"_Precip_mean"))')

    for f in zonalStatsPrecip.selectedFeatures():
        context = QgsExpressionContext()
        context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(zonalStatsPrecip))
        context.setFeature(f)
        f['_Precip_mean'] = expression.evaluate(context)
        zonalStatsPrecip.updateFeature(f)
    zonalStatsPrecip.commitChanges()
    zonalStatsPrecip.setSubsetString('')

    QgsProject.instance().removeMapLayer(clone_zonalStatsMin)
    QgsProject.instance().removeMapLayer(clone_zonalStatsMax)
    QgsProject.instance().removeMapLayer(clone_zonalStatsPrecip)
    
    zonalStatsPrecip.selectAll()
    
    dateToday_format = date[6:8] + '/' + date[4:6] + '/' + date[:4]
    conn = psycopg2.connect(
       database="ayishi", user='developer', password='ObuEm8Ap', host='165.227.135.116', port= '5432'
    )
    conn.autocommit = True
    cursor = conn.cursor()

    command = "SET datestyle = dmy"
    cursor.execute(command)
    conn.commit()

    for feat in zonalStatsPrecip.selectedFeatures():
        avgtemp = (feat['_Min_mean'] + feat['_Max_mean'])/2
        command = "INSERT INTO agriculture_communemeteo VALUES (default,'{}',{},{},{},{},{})".format(dateToday_format, feat['_Min_mean'], avgtemp, feat['_Max_mean'], feat['_Precip_mean'], feat['id'])
        cursor.execute(command)
        conn.commit()
    conn.close()
    
    QgsProject.instance().removeMapLayer(zonalStatsPrecip)
    QgsProject.instance().removeMapLayer(tinPrecip)
    del zonalStatsPrecip
    del zonalStatsMax
    del zonalStatsMin
    del stationsLayerReproj
    del tinMin
    del tinMax
    del tinPrecip