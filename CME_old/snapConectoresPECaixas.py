## work around para fazer import da biblioteca das funções :/
#exec(open('D:/OneDriveGW/PROJECTOS/CME_ARM/scripts/greenWorldPyQgis.py').read()) ### este path tem de ser editado

deleteTemporaryLayers()

dictErrorMessages = {
    'Conector - Tamanho':"'Conector com mais de 1.5 m'",
    'Conector - isolado':"'Conector não interseta caixa, ou PE'",
    'PE - snap GPS':"'Ponto de Entrega não snappado a um ponto GPS'",
    'PE - snap Canal ou Conector':"'Ponto de Entrega não interseta canal nem conector'",
    'Tornadoiro - fora da parcela':"'Tornadoiro fora da parcela'"
}

layerConector = QgsProject.instance().mapLayersByName('CONECTOR')[0]
layerPE = QgsProject.instance().mapLayersByName('PONTOENTREGA')[0]
layerCaixa = QgsProject.instance().mapLayersByName('CAIXA')[0]
layerGPS = QgsProject.instance().mapLayersByName('PONTOSGPSCME')[0]
layerTornadoiro = QgsProject.instance().mapLayersByName('TORNADOIRO')[0]
layerCanal = QgsProject.instance().mapLayersByName('CANAL')[0]

#createWKTField(layerGPS)
#updateGeometryFromWKT(layerGPS)

### SNAP Pontos Entrega ao GPS
tolerance = 0.1
behavior = 3

snapPE_GPS = processing.run("native:snapgeometries", {
    'INPUT':layerPE,
    'REFERENCE_LAYER':layerGPS,
    'TOLERANCE':tolerance,
    'BEHAVIOR':3, #behavior
    'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
})['OUTPUT']

## 1.1. field calculator caixas wkt
createWKTField(snapPE_GPS)
QgsProject.instance().addMapLayer(snapPE_GPS)
snapPE_GPS.setName('PE')

#### Conectores ligados a caixas e PE
conectorSnapPE = processing.run("native:snapgeometries", {
    'INPUT':layerConector,
    'REFERENCE_LAYER':snapPE_GPS,
    'TOLERANCE':tolerance,
    'BEHAVIOR':behavior,
    'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
})['OUTPUT']

#QgsProject.instance().addMapLayer(conectorSnapPE)

conectorSnapFinal = processing.run("native:snapgeometries", {
    'INPUT':conectorSnapPE,
    'REFERENCE_LAYER':layerCaixa,
    'TOLERANCE':tolerance,
    'BEHAVIOR':behavior,
    'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
})['OUTPUT']

createWKTField(conectorSnapFinal)

QgsProject.instance().addMapLayer(conectorSnapFinal)
conectorSnapFinal.setName('CONECTOR2')
#### Canais ligados a PE
behavior = 3

canalSnapPE = processing.run("native:snapgeometries", {
    'INPUT':layerCanal,
    'REFERENCE_LAYER':snapPE_GPS,
    'TOLERANCE':tolerance,
    'BEHAVIOR':behavior,
    'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
})['OUTPUT']

createWKTField(canalSnapPE)
QgsProject.instance().addMapLayer(canalSnapPE)
canalSnapPE.setName('CANAL2')

## atualizar a geometria dos PE (snappados aos pontos gps)
createJoin(snapPE_GPS, layerPE)
updateGeometryFromWKT(layerPE)

## atualizar a geometria dos conectores (snappados a PE e a caixas)
createJoin(conectorSnapFinal, layerConector)
updateGeometryFromWKT(layerConector)

## atualizar a geometria dos conectores (snappados a PE e a caixas)
createJoin(canalSnapPE, layerCanal)
updateGeometryFromWKT(layerCanal)

## ERROS de PE não snappado a GPS
layerPE.setSubsetString('"MODO_IDENTIFICACAO" = 5 AND "SITUACAO_EXISTENTE" != 3')
gpsString = 'PONTOSGPSCME'
cxbufferString = 'CAIXAbuffer'
expression = "NOT (overlay_intersects('{}') OR overlay_within('{}'))".format(gpsString, cxbufferString)
layerPE.selectByExpression(expression)

erroBufferPEGPS = errorBuffer(layerPE, dictErrorMessages['PE - snap GPS'])
QgsProject.instance().addMapLayer(erroBufferPEGPS)
erroBufferPEGPS.setName(dictErrorMessages['PE - snap GPS'])
layerPE.setSubsetString('"SITUACAO_EXISTENTE" != 3')
layerPE.removeSelection()

## ERROS de PE não snappado Canal ou conector
canalString = 'CANAL'
conectorString = 'CONECTOR'
expression = "(intersecting_geom_count('{}')+intersecting_geom_count('{}'))=0".format(canalString, conectorString)
#expression = "NOT (overlay_intersects('{}') OR overlay_intersects('{}'))".format(canalString, conectorString)
snapPE_GPS.selectByExpression(expression)

erroBufferPE_canal_conector = errorBuffer(snapPE_GPS, dictErrorMessages['PE - snap Canal ou Conector'])
QgsProject.instance().addMapLayer(erroBufferPE_canal_conector)
erroBufferPE_canal_conector.setName(dictErrorMessages['PE - snap Canal ou Conector'])
snapPE_GPS.removeSelection()

## ERROS de Conector com mais de 1.5 m
expression = '$length > 1.5'
conectorSnapFinal.selectByExpression(expression)

erroBufferConectorGrande = errorBuffer(conectorSnapFinal, dictErrorMessages['Conector - Tamanho'])
QgsProject.instance().addMapLayer(erroBufferConectorGrande)
erroBufferConectorGrande.setName(dictErrorMessages['Conector - Tamanho'])
conectorSnapFinal.removeSelection()

## ERROS de Conector não intersetando canal ou caixa
expression = '"SITUACAO_EXISTENTE" != 3' + " AND NOT (overlay_touches('CAIXA') OR overlay_touches('CANAL')) OR NOT overlay_touches('PE')"
conectorSnapFinal.selectByExpression(expression)

erroBufferConectorIsolado = errorBuffer(conectorSnapFinal, dictErrorMessages['Conector - isolado'])
QgsProject.instance().addMapLayer(erroBufferConectorIsolado)
erroBufferConectorIsolado.setName(dictErrorMessages['Conector - isolado'])
conectorSnapFinal.removeSelection()

## ERROS de Tornadoiro
expression = '"CODIGO_PC" = ' + "geomwithin('PARCELA', 'CODIGO_PC') or " + '"CODIGO_PC" =' + "geomwithin('PONTOENTREGAbuffer', 'CODIGO_PC')"
layerTornadoiro.selectByExpression(expression)
layerTornadoiro.invertSelection()

erroBufferTornadoiro = errorBuffer(layerTornadoiro, dictErrorMessages['Tornadoiro - fora da parcela'])
QgsProject.instance().addMapLayer(erroBufferTornadoiro)
erroBufferTornadoiro.setName(dictErrorMessages['Tornadoiro - fora da parcela'])
layerTornadoiro.removeSelection()

### atualizar a geometria dos PE (snappados aos pontos gps)
#createJoin(snapPE_GPS, layerPE)
#updateGeometryFromWKT(layerPE)
#
### atualizar a geometria dos conectores (snappados a PE e a caixas)
#createJoin(conectorSnapFinal, layerConector)
#updateGeometryFromWKT(layerConector)
#
### atualizar a geometria dos conectores (snappados a PE e a caixas)
#createJoin(canalSnapPE, layerCanal)
#updateGeometryFromWKT(layerCanal)