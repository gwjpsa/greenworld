import numpy as np

layer_tornadoiro_og = QgsProject.instance().mapLayersByName('03_06R05_CQ — VRTORNADOIRO')[0]
layer_PE = QgsProject.instance().mapLayersByName('03_06R05_CQ — VRPONTOENTREGA')[0]

####### duplicate layer
layer_tornadoiro = createDuplicateLayer(layer_tornadoiro_og, 'Point')
#################

createWKTField(layer_tornadoiro)

context_Tornadoiro = QgsExpressionContext()
context_Tornadoiro.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer_tornadoiro))

for PE_feat in layer_PE.getFeatures():
    
    pe_pt = PE_feat.geometry().vertexAt(0)
    
    codigo_pc = PE_feat['CODIGO_PC']
    expression = '"CODIGO_PC" = \'{}\''.format(codigo_pc)
    layer_tornadoiro.selectByExpression(expression)
    
    layer_tornadoiro.startEditing()
    
    for tornadoiro_feat in layer_tornadoiro.selectedFeatures():
        
        context_Tornadoiro.setFeature(tornadoiro_feat)
        
        tornadoiro_pt = tornadoiro_feat.geometry().vertexAt(0)
        
        distance = tornadoiro_pt.distance(pe_pt)
        print(distance)
        maxDist = 10
        
        if distance > 1 and distance < maxDist:
            
            pe_ptX = pe_pt.x()
            pe_ptY = pe_pt.y()
            
            tornadoiro_ptX = tornadoiro_pt.x()
            tornadoiro_ptY = tornadoiro_pt.y()
            
            len_limit = 1
            
            try:
                alpha = np.arctan((tornadoiro_ptY - pe_ptY)/(tornadoiro_ptX - pe_ptX))

                if tornadoiro_ptX < pe_ptX:
                    alpha = alpha - np.pi
                
            except:
                if tornadoiro_ptY > pe_ptY:
                    alpha = 0
                else:
                    alpha = np.pi
            
            #print(alpha)
            
            if alpha < np.pi/2:
                newX = np.round(pe_ptX + len_limit * np.cos(alpha), 8)
                newY = np.round(pe_ptY + len_limit * np.sin(alpha), 8)
            elif alpha >= np.pi/2 and alpha < np.pi:
                newX = np.round(pe_ptX + len_limit * np.cos(alpha), 8)
                newY = np.round(pe_ptY - len_limit * np.sin(alpha), 8)
            elif alpha >= np.pi and alpha < 3*np.pi/2:
                newX = np.round(pe_ptX - len_limit * np.cos(alpha), 8)
                newY = np.round(pe_ptY - len_limit * np.sin(alpha), 8)
            else:
                newX = np.round(pe_ptX - len_limit * np.cos(alpha), 8)
                newY = np.round(pe_ptY + len_limit * np.sin(alpha), 8)
                
            newWKT = QgsExpression('\'MultiPointZ (({} {} 0))\''.format(newX, newY))
            
            tornadoiro_feat['wkt'] = newWKT.evaluate(context_Tornadoiro)
            layer_tornadoiro.updateFeature(tornadoiro_feat)
    
updateGeometryFromWKT(layer_tornadoiro)
layer_tornadoiro.setName('tornadoiros_duplicados')
## executar depois de validar os tornadoiros manualmente
#createWKTField(layer_tornadoiro)
#createJoin(layer_tornadoiro, layer_tornadoiro_og)
#updateGeometryFromWKT(layer_tornadoiro_og)