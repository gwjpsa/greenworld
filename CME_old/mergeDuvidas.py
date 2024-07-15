import processing
#todas as layers devem estar no modo edição desligado

#path = '//GW-RS-PC/OneDriveGW/PROJECTOS/CME_ARM/1_REGADEIRAS/01_03R18_03R19_03R21_GAB/duvidas_01_03R18_03R19_03R21.gpkg|layername=duvidas'# path (gpkg|layer)
layer = QgsProject.instance().mapLayersByName('DUVIDAS')[0] # nome layer gpkg

# toggle editing mode (ON)
#edit_action = iface.mainWindow().findChild(QAction, "mActionToggleEditing")
#edit_action.trigger()

layer.startEditing()

# percorrer todas as features da layer selecionada
listAggregatedFeatures = []

for f in layer.getFeatures():
    
    layer.removeSelection() # remover qualquer possível seleção que esteja feita
    selFeat = layer.select(f.id()) # selecionar a feature sobre a qual se está a iterar
    
    # select by location com base na feature selecionada
    processing.run("native:selectbylocation", {
        'INPUT': layer.source(),
        # parâmetros do INTERSECT copiado do log desta operação quando executada manualmente
        'INTERSECT' : QgsProcessingFeatureSourceDefinition(
            layer.source(),
            selectedFeaturesOnly=True, # procurar features com base na feature selecionada
            featureLimit=-1,
            geometryCheck=QgsFeatureRequest.GeometryAbortOnInvalid
        ),
        'METHOD' : 0, # fazer uma nova seleção por iteração
        'PREDICATE' : [3], # selecionar apenas features iguais à feature sobre a qual se está a iterar(EQUAL)
    })
    
    agregate = processing.run("native:aggregate", {
        'INPUT':QgsProcessingFeatureSourceDefinition(
            layer.source(),
            selectedFeaturesOnly=True,
            featureLimit=-1,
            geometryCheck=QgsFeatureRequest.GeometryAbortOnInvalid
        ),
        'GROUP_BY':'NULL',
        'AGGREGATES':[
            {'aggregate': 'sum','delimiter': ',','input': '"ID"','length': 0,'name': 'ID1','precision': 0,'sub_type': 0,'type': 4,'type_name': 'int8'},
            {'aggregate': 'concatenate','delimiter': ',','input': '"Duvidas_Gabinete"','length': 65535,'name': 'Duvidas_Gabinete','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},
            {'aggregate': 'concatenate','delimiter': ',','input': '"Resposta_Campo"','length': 255,'name': 'Resposta_Campo','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}
        ],
        'OUTPUT':'TEMPORARY_OUTPUT'
    })['OUTPUT']
    
    listAggregatedFeatures.append(agregate)
    
mergeLayer = processing.run("native:mergevectorlayers", {
    'LAYERS':listAggregatedFeatures,
    'CRS':None,
    'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
})['OUTPUT']

#QgsProject.instance().addMapLayer(mergeLayer)

uniqueFeatures = processing.run("native:deleteduplicategeometries", {
    'INPUT':mergeLayer,
    'OUTPUT':'TEMPORARY_OUTPUT'
})['OUTPUT']
QgsProject.instance().addMapLayer(uniqueFeatures)