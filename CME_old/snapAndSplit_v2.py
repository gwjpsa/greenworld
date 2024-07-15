
Q
# -*- coding: utf-8 -*-
import processing

QgsProj = QgsProject.instance()

## eliminar layers temporárias
layers = QgsProject.instance().mapLayers()
for layer_id, layer in layers.items():
    if 'memory?' in layer.dataProvider().dataSourceUri():
        # print(layer.name())
        QgsProj.removeMapLayer(QgsProj.mapLayersByName(layer.name())[0].id())

## 1. Snap Caixas a pontos GPS --> cx_snap

layerGPS = QgsProject.instance().mapLayersByName('VRPONTOSGPSCME')[0]
layerCaixa = QgsProject.instance().mapLayersByName('VRCAIXA')[0]
layerCanais = QgsProject.instance().mapLayersByName('VRCANAL')[0]

#layerGPS = QgsProject.instance().mapLayersByName('gps')[0]
#layerCaixa = QgsProject.instance().mapLayersByName('caixas')[0]
#layerCanais = QgsProject.instance().mapLayersByName('linhas')[0]

createWKTField(layerGPS)
updateGeometryFromWKT(layerGPS)

tolerance = 0.1
behavior = 0

cx_snap = processing.run("native:snapgeometries", {
    'INPUT':layerCaixa,
    'REFERENCE_LAYER':layerGPS,
    'TOLERANCE':tolerance,
    'BEHAVIOR':behavior,
    'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
})['OUTPUT']

#cx_snap = processing.run("native:snapgeometries", {'INPUT':QgsProcessingFeatureSourceDefinition('C:/Users/joaos/OneDrive/Ambiente de Trabalho/QGIS_TESTES/01_03R18_03R19_03R21_GAB - Cópia.gpkg|layername=VRCAIXA', selectedFeaturesOnly=False, featureLimit=-1, flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck, geometryCheck=QgsFeatureRequest.GeometryNoCheck),'REFERENCE_LAYER':'C:/Users/joaos/OneDrive/Ambiente de Trabalho/QGIS_TESTES/01_03R18_03R19_03R21_GAB - Cópia.gpkg|layername=VRPONTOSGPSCME','TOLERANCE':0.1,'BEHAVIOR':0,'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']

pr = cx_snap.dataProvider()

## 1.1. field calculator caixas wkt
cx_snap.selectAll()
cx_snap.startEditing()

pr.addAttributes([QgsField('wkt', QVariant.String)])
cx_snap.updateFields()

expression = QgsExpression('geom_to_wkt($geometry)')
## expression = QgsExpression("'ola'") # teste

for f in cx_snap.selectedFeatures():
    context = QgsExpressionContext()
    context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(cx_snap))
    context.setFeature(f)
    f['wkt'] = expression.evaluate(context)
    cx_snap.updateFeature(f)
cx_snap.commitChanges()

QgsProject.instance().addMapLayer(cx_snap)

## 2. Snap canais às caixas (cx_snap) --> canais_snap
# não cria vertices
tolerance = 0.2
behavior = 3

canais_snap_0 = processing.run("native:snapgeometries", {
    'INPUT':layerCanais,
    'REFERENCE_LAYER':cx_snap,
    'TOLERANCE':tolerance,
    'BEHAVIOR':behavior,
    'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
})['OUTPUT']

#QgsProject.instance().addMapLayer(canais_snap_0)

## 2. Snap canais às caixas (cx_snap) --> canais_snap
# cria vertices tolerancia mais baixa
tolerance = 0.1
behavior = 1

canais_snap = processing.run("native:snapgeometries", {
    'INPUT':canais_snap_0,
    'REFERENCE_LAYER':cx_snap,
    'TOLERANCE':tolerance,
    'BEHAVIOR':behavior,
    'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
})['OUTPUT']

## 3.1. Buffer caixas snappadas
buffer_aux = processing.run("native:buffer", {
    'INPUT':cx_snap,
    'DISTANCE':0.01, ## distancia de 1 cm
    'SEGMENTS':5,
    'END_CAP_STYLE':0,
    'JOIN_STYLE':0,
    'MITER_LIMIT':2,
    'DISSOLVE':False,
    'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
})['OUTPUT']

## 3.2. Polygon to lines
line_buffer = processing.run("saga:convertpolygonstolines", {
    'POLYGONS':buffer_aux,
    'LINES':QgsProcessing.TEMPORARY_OUTPUT
})['LINES']

## 3.3 Split Lines
canaisSplited = processing.run("native:splitwithlines", {
    'INPUT':canais_snap,
    'LINES':line_buffer,
    'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
})['OUTPUT']

## 3.4 Select by location & delete selected features
canaisSplited.startEditing()

processing.run("native:selectbylocation", {
    'INPUT':canaisSplited,
    'PREDICATE':[0],
    'INTERSECT':cx_snap,
    'METHOD':0
})

for f in canaisSplited.selectedFeatures():
    canaisSplited.deleteFeature(f.id())

canaisSplited.commitChanges()
## 4. Snap canais às caixas

tolerance = 0.1
behavior = 1

canaisSnap = processing.run("native:snapgeometries", {
    'INPUT':canaisSplited,
    'REFERENCE_LAYER':cx_snap,
    'TOLERANCE':tolerance,
    'BEHAVIOR':behavior,
    'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
})['OUTPUT']

## 4.1. field calculator wkt canais
canaisSnap.selectAll()
canaisSnap.startEditing()

pr = canaisSnap.dataProvider()
pr.addAttributes([QgsField('wkt', QVariant.String)])
canaisSnap.updateFields()

expression = QgsExpression('geom_to_wkt($geometry)')
## expression = QgsExpression("'ola'") # teste

for f in canaisSnap.selectedFeatures():
    context = QgsExpressionContext()
    context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(canaisSnap))
    context.setFeature(f)
    f['wkt'] = expression.evaluate(context)
    canaisSnap.updateFeature(f)
canaisSnap.commitChanges()

QgsProject.instance().addMapLayer(canaisSnap)
canaisSnap.setName('Snapped geometry c')
## 5. Extrair os vértices

## inicialização das listas que vão conter:
startingVerticesByPart = [] ## os vértices iniciais de cada troço de cada feature
finalVerticesByPart = [] ## os vértices finais de cada troço de cada feature

## ciclo para iterar sobre cada feature na layer dos canais
for feature in canaisSnap.getFeatures():
    aux = [] ## variável auxiliar para armazenar os vértices de cada troço de cada feature
    ## ciclo para iterar sobre cada troço de cada uma das features
    if feature.geometry().type() == 1:
        for pnt in feature.geometry().asPolyline():
            ## coordenadas de cada vértice de cada troço
            print(pnt.x(), pnt.y())
            ## armazenar o vértice (PointXY) na lista auxiliar
            feat = QgsFeature()
            feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(pnt)))
            aux.append((pnt.x(), pnt.y()))
        ## armazenar a lista de vértices dos troços (da lista auxiliar)
        startingVerticesByPart+=aux[:-1] ## iniciais
        finalVerticesByPart+=aux[1:] ## finais

uniqueStartVert, duplicateStartVert = getUniqueAndDuplicated(startingVerticesByPart)
uniqueFinalVert, duplicateFinalVert = getUniqueAndDuplicated(finalVerticesByPart)

## inicialização da layer temporária dos pontos iniciais e/ou finais (que são duplicados) de cada troço
dupVertLayer = QgsVectorLayer("Point?crs=epsg:3061", "temporary_duplicated_vertices", "memory")
QgsProject.instance().addMapLayer(dupVertLayer, True)
dupVertLayer.startEditing()

## pontos iniciais
if len(duplicateStartVert) > 0:
    for elem in duplicateStartVert:
        feat = QgsFeature()
        feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(elem[0],elem[1])))
        dupVertLayer.addFeature(feat)
    
## pontos finais
if len(duplicateFinalVert) > 0:
    for elem in duplicateStartVert:
        feat = QgsFeature()
        feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(elem[0],elem[1])))
        dupVertLayer.addFeature(feat)

dupVertLayer.commitChanges()

processing.run("native:selectbylocation", {
    'INPUT':dupVertLayer,
    'PREDICATE':[2],
    'INTERSECT':cx_snap,
    'METHOD':1
})

errors = dupVertLayer.selectedFeatures()

## inicialização da layer dos buffers dos vértices iniciais e finais de cada feature
testBuffer=QgsVectorLayer("Polygon?crs=epsg:3061", "possible errors", "memory")
testBuffer.startEditing()
pr = testBuffer.dataProvider()
pr.addAttributes([QgsField("id", QVariant.Int)])
testBuffer.updateFields()
QgsProject.instance().addMapLayer(testBuffer, True)

dist = 1.5 ## parâmetro distance do buffer
numSegm = 5 ## numéro de segmentos para desenhar 1/4 da circunferência
c = 1
for ft in errors:
    n_ft = QgsFeature()
    geom = ft.geometry()
    ## criação do buffer para cada feature (ponto)
    buff = geom.buffer(dist, numSegm)
    n_ft.setAttributes([c])
    n_ft.setGeometry(buff)
    ## adição do buffer criado à layer criada
    testBuffer.addFeature(n_ft)
    c+=1
## gravar as alterações
testBuffer.commitChanges()
######################################################