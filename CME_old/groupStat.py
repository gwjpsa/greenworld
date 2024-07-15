import csv

lista = []

with open("C:/Users/joaos/OneDrive/Ambiente de Trabalho/04R10_04R15_04R18_04R19/groupStat.csv", 'r') as file:
  csvreader = csv.reader(file, delimiter=';')
  header = []
  header = next(csvreader)
  for row in csvreader:
      if row != []:
          if int(row[2]) > 1:
              lista.append([row[0], row[1], int(row[2])])

layerCanais = QgsProject.instance().mapLayersByName('VRCANAL')[0]
canaisSnap = QgsProject.instance().mapLayersByName('Snapped geometry c')[0]
canaisSnap.startEditing()

context = QgsExpressionContext()
context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(canaisSnap))

for c in lista:
    expression = '"ID1"=' + c[0]
    canaisSnap.selectByExpression(expression)
    i = 0
    for f in canaisSnap.selectedFeatures()[1:]:
        context.setFeature(f)
        i+=1
        newID1Calc = QgsExpression('1230000000 + "ID1"*100 + ' + str(i))
        f['ID1'] = newID1Calc.evaluate(context)
        newIPID = QgsExpression('NULL')
        f['IPID'] = newIPID.evaluate(context)
        newCODCANAL = QgsExpression('NULL')
        f['CODIGO_CANAL'] = newCODCANAL.evaluate(context)
        newSitExist = QgsExpression('1')
        f['SITUACAO_EXISTENTE'] = newSitExist.evaluate(context)
        canaisSnap.updateFeature(f)
canaisSnap.commitChanges()

## Join canais novos (canaisSnap) -- VRCANAL
l1_Field="ID1"
l2_Field="ID1"
joinObjectCanal=QgsVectorLayerJoinInfo()
joinObjectCanal.setJoinFieldName(l1_Field)
joinObjectCanal.setTargetFieldName(l2_Field)
joinObjectCanal.setJoinLayerId(canaisSnap.id())
joinObjectCanal.setJoinFieldNamesSubset(["wkt"])
joinObjectCanal.setUsingMemoryCache(True)
joinObjectCanal.setJoinLayer(canaisSnap)
layerCanais.addJoin(joinObjectCanal)

## Join caixas snappadas -- VRCAIXA_auxiliar
l1_Field="ID1"
l2_Field="ID1"
joinObjectCaixa=QgsVectorLayerJoinInfo()
joinObjectCaixa.setJoinFieldName(l1_Field)
joinObjectCaixa.setTargetFieldName(l2_Field)
joinObjectCaixa.setJoinLayerId(cx_snap.id())
joinObjectCaixa.setJoinFieldNamesSubset(["wkt"])
joinObjectCaixa.setUsingMemoryCache(True)
joinObjectCaixa.setJoinLayer(cx_snap)
layerCaixa.addJoin(joinObjectCaixa)

## change geometry CANAIS
layerCanais.startEditing()

for f in layerCanais.getFeatures():
    wktGeom = f.attributes()[-1]
    try:
        layerCanais.changeGeometry(f.id(),QgsGeometry.fromWkt(wktGeom))
    except:
        pass
layerCanais.commitChanges()

## change geometry CAIXAS
layerCaixa.startEditing()

for f in layerCaixa.getFeatures():
    wktGeom = f.attributes()[-1]
    try:
        layerCaixa.changeGeometry(f.id(),QgsGeometry.fromWkt(wktGeom))
    except:
        pass
layerCaixa.commitChanges()

pr = layerCanais.dataProvider()
pr.addAttributes([QgsField('wkt', QVariant.String)])
layerCanais.updateFields()

canaisSnap.selectByExpression('"ID1" > 1230000000')
layerCanais.startEditing()
newFeats = canaisSnap.selectedFeatures()

pr = layerCanais.dataProvider()
pr.addFeatures(newFeats)
layerCanais.commitChanges()

expression = QgsExpression('"Snapped geometry c_wkt"')
## expression = QgsExpression("'ola'") # teste

for f in layerCanais.selectedFeatures():
    context = QgsExpressionContext()
    context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layerCanais))
    context.setFeature(f)
    f['wkt'] = expression.evaluate(context)
    layerCanais.updateFeature(f)
layerCanais.commitChanges()

### wkt no VRCANAL
layerCanais.selectAll()
layerCanais.startEditing()

for f in layerCanais.getFeatures():
    wktGeom = f.attributes()[-2]
    try:
        layerCanais.changeGeometry(f.id(),QgsGeometry.fromWkt(wktGeom))
    except:
        pass
layerCanais.commitChanges()