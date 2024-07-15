## work around para fazer import da biblioteca das funções :/
#exec(open('D:/OneDriveGW/PROJECTOS/CME_ARM/scripts/greenWorldPyQgis.py').read())

deleteTemporaryLayers()

### PARCELA ###
layerParcela = QgsProject.instance().mapLayersByName('VRPARCELA')[0]
entidade = 'Parcela'
errosParcelas = []

## OBSERVAÇÕES
field = 'OBSERVACOES'
oldAttribute = "'-'"
newAttribute = 'NULL'
autoFieldCalculator(layerParcela, field, oldAttribute, newAttribute)

### Field Calulator (posteriores às queries, de modo a que os centroids já tenham estes novos atributos)
## SITUAÇÃO CONFLITO
field = 'SITUACAO_CONFLITO'
oldAttr = NULL
newAttr = 'Inexistente'
autoFieldCalculator(layerParcela, field, oldAttr, newAttr)

## ORIGEM_AGUA
field = 'ORIGEM_AGUA'
oldAttr = NULL
newAttr = '0'
autoFieldCalculator(layerParcela, field, oldAttr, newAttr)

## COD CLIENTE CONFLITO
field = 'COD_CLIENTE_CONFLITO'
oldAttr = 0
newAttr = 'NULL'
autoFieldCalculator(layerParcela, field, oldAttr, newAttr)

## COD CLIENTE DECLARANTE 111111111
query = '"COD_CLIENTE_DECLARANTE" = 111111111'
layerParcela.selectByExpression(query)

context = QgsExpressionContext()
context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layerParcela))

for f in layerParcela.selectedFeatures():
    context.setFeature(f)
    
    newMODO_IDENTIFICACAO = QgsExpression('8') # Informação verbal
    f['MODO_IDENTIFICACAO'] = newMODO_IDENTIFICACAO
    
    newTITULARIDADE = QgsExpression('0') # Não conhecido
    f['TITULARIDADE'] = newTITULARIDADE
    
    newRELACAO_COM_TITULAR = QgsExpression('142') # levadeiro
    f['RELACAO_COM_TITULAR'] = newRELACAO_COM_TITULAR
    
    newSITUACAO_CONFLITO = QgsExpression('0') # Não conhecido
    f['SITUACAO_CONFLITO'] = newSITUACAO_CONFLITO
    
    newCOD_CLIENTE_CONFLITO = QgsExpression('NULL') # NULL
    f['COD_CLIENTE_CONFLITO'] = newSITUACAO_CONFLITO
    
    newORIGEM_AGUA = QgsExpression('0') # Não conhecido
    f['ORIGEM_AGUA'] = newORIGEM_AGUA
    
    if f['ESTUFA'] == 'Sim' or f['ESTUFA'] == 'Não':
        pass
    else:
        newESTUFA = QgsExpression('Não conhecido') # Não conhecido
        f['ESTUFA'] = newESTUFA
    
    newAPRESENTACAO_DOCUMENTOS = QgsExpression('Não') # Não
    f['APRESENTACAO_DOCUMENTOS'] = newAPRESENTACAO_DOCUMENTOS
    
    if f['OBSERVACOES'] == NULL:
        newOBSERVACOES = QgsExpression('Não compareceu.') # Não compareceu
    elif 'Não compareceu' in f['OBSERVACOES']:
        newOBSERVACOES = QgsExpression(str(f['OBSERVACOES']))
    else:
        newOBSERVACOES = QgsExpression('Não compareceu. ' + str(f['OBSERVACOES'])) # Não compareceu
    f['OBSERVACOES'] = newOBSERVACOES

## COD CLIENTE DECLARANTE 0
query = '"COD_CLIENTE_DECLARANTE" = 0'
layerParcela.selectByExpression(query)

context = QgsExpressionContext()
context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layerParcela))

for f in layerParcela.selectedFeatures():
    context.setFeature(f)
    
    newMODO_IDENTIFICACAO = QgsExpression('8') # Informação verbal
    f['MODO_IDENTIFICACAO'] = newMODO_IDENTIFICACAO
    
    newTITULARIDADE = QgsExpression('0') # Não conhecido
    f['TITULARIDADE'] = newTITULARIDADE
    
    newRELACAO_COM_TITULAR = QgsExpression('0') # Não conhecido
    f['RELACAO_COM_TITULAR'] = newRELACAO_COM_TITULAR
    
    newSITUACAO_CONFLITO = QgsExpression('0') # Não conhecido
    f['TITULARIDADE'] = newSITUACAO_CONFLITO
    
    newCOD_CLIENTE_CONFLITO = QgsExpression('NULL') # NULL
    f['COD_CLIENTE_CONFLITO'] = newSITUACAO_CONFLITO
    
    newTIPO_REGA = QgsExpression('0') # Não conhecido
    f['TIPO_REGA'] = newTIPO_REGA
    
    newORIGEM_AGUA = QgsExpression('Não conhecido') # Não conhecido
    f['ORIGEM_AGUA'] = newORIGEM_AGUA
    
    newESTUFA = QgsExpression('Não conhecido') # Não conhecido
    f['ESTUFA'] = newESTUFA
    
    newAPRESENTACAO_DOCUMENTOS = QgsExpression('Não') # Não
    f['APRESENTACAO_DOCUMENTOS'] = newAPRESENTACAO_DOCUMENTOS
    
    if f['OBSERVACOES'] == NULL:
        newOBSERVACOES = QgsExpression('Não compareceu. Localização Desconhecida.') # Não compareceu
    elif 'Não compareceu. Localização Desconhecida' in f['OBSERVACOES']:
        newOBSERVACOES = QgsExpression(str(f['OBSERVACOES']))
    else:
        newOBSERVACOES = QgsExpression('Não compareceu. Localização Desconhecida. ' + str(f['OBSERVACOES'])) # Não compareceu
    f['OBSERVACOES'] = newOBSERVACOES

## SITUACAO_EXISTENTE
field = 'SITUACAO_EXISTENTE'
dictSituacaoExistente = {
    0:"\"--Não conhecido--\"'",
    3:"\"Eliminar\"'",
    4:"\"Sem alteração\"'",
    5:"\"Validar\"'",
    6:"\"Confirmar\"'",
    7:"\"Partilha\"'",
    NULL:"NULL'"
}

errosSitExistente = getAttributeErrors(layerParcela, entidade, field, dictSituacaoExistente)

errosParcelas+=errosSitExistente

layerParcela.setSubsetString('"SITUACAO_EXISTENTE" = 1 OR "SITUACAO_EXISTENTE" = 2')
#layerParcela.setSubsetString('"SITUACAO_EXISTENTE" = 1 OR "SITUACAO_EXISTENTE" = 2 AND "COD_CLIENTE_DECLARANTE" != 0 AND "COD_CLIENTE_DECLARANTE" != 111111111')

### Centroids auxiliares para fazer os buffers
centroidPARCELA = processing.run("native:centroids", {
    'INPUT':layerParcela.source(),
    'ALL_PARTS':True,
    'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
})['OUTPUT']
QgsProject.instance().addMapLayer(centroidPARCELA)

centroidPARCELA.setSubsetString('"SITUACAO_EXISTENTE" = 1 OR "SITUACAO_EXISTENTE" = 2 AND "COD_CLIENTE_DECLARANTE" != 0 AND "COD_CLIENTE_DECLARANTE" != 111111111')

## MODO_IDENTIFICACAO
field = 'MODO_IDENTIFICACAO'
dictModoIdentificacao_PARCELA = {
    0:"\"--Não conhecido--\"'",
    1:"\"Indefinido\"'",
    NULL:"NULL'"
}

errosModoIdentificacao_Parcelas = getAttributeErrors(centroidPARCELA, entidade, field, dictModoIdentificacao_PARCELA)

errosParcelas+=errosModoIdentificacao_Parcelas

## SITUAÇÃO CONFLITO
field = 'SITUACAO_CONFLITO'
dictSituacaoConflito_PARCELA = {
    0:"\"--Não conhecido--\"'"
}

errosSituacaoConflito_Parcelas = getAttributeErrors(centroidPARCELA, entidade, field, dictSituacaoConflito_PARCELA)

errosParcelas+=errosSituacaoConflito_Parcelas

### ORIGEM_AGUA
#field = 'ORIGEM_AGUA'
#dictOrigemAgua_PARCELA = {
#    NULL:"NULL'"
#}
#
#errosOrigemAgua_Parcelas = getAttributeErrors(centroidPARCELA, entidade, field, dictOrigemAgua_PARCELA)
#
#errosParcelas+=errosOrigemAgua_Parcelas

centroidPARCELA.setSubsetString('"SITUACAO_EXISTENTE" = 1 OR "SITUACAO_EXISTENTE" = 2')

## TIPO_REGA
field = 'TIPO_REGA'
dictTipoRega_PARCELA = {
    NULL:"NULL'"
}

errosTipoRega_Parcelas = getAttributeErrors(centroidPARCELA, entidade, field, dictTipoRega_PARCELA)

errosParcelas+=errosTipoRega_Parcelas

## USO_SOLO
field = 'USO_SOLO'
dictUsoSolo_PARCELA = {
    NULL:"NULL'"
}

errosUsoSolo_Parcelas = getAttributeErrors(centroidPARCELA, entidade, field, dictUsoSolo_PARCELA)

errosParcelas+=errosUsoSolo_Parcelas

## ESTUFA
field = 'ESTUFA'
dictEstufa_PARCELA = {
    NULL:"NULL'"
}

errosEstufa_Parcelas = getAttributeErrors(centroidPARCELA, entidade, field, dictEstufa_PARCELA)

errosParcelas+=errosEstufa_Parcelas

## APRESENTAÇÃO DOCUMENTOS
field = 'APRESENTACAO_DOCUMENTOS'
dictApresentacaoDocumentos_PARCELA = {
    NULL:"NULL'"
}

errosApresentacaoDocumentos_Parcelas = getAttributeErrors(centroidPARCELA, entidade, field, dictApresentacaoDocumentos_PARCELA)

errosParcelas+=errosApresentacaoDocumentos_Parcelas

centroidPARCELA.selectByExpression(
'"APRESENTACAO_DOCUMENTOS" = ' + "'{}' AND ".format('Sim') +'(\
"FREGUESIA_CONSERVATORIA" is NULL AND \
"FREGUESIA_FINANCAS" is NULL AND \
"ARTIGO_FINANCAS" is NULL AND \
"REPARTICAO_FINANCAS" is NULL AND\
"REGISTO_NUM_LIVRO" is NULL AND \
"REGISTO_DESC_FICHA" is NULL AND \
"REGISTO_DESC_LIVRO" is NULL AND\
"PREDIO" is NULL AND\
"FRACCAO" is NULL AND\
"SECCAO__MM" is NULL)'
)

errorMsg = "'Parcela com campo APRESENTACAO_DOCUMENTOS1 " + '"Sim" e campos dos Documentos NULL' + "'"

errosApresentacaoDocumentosSimNULL_Parcelas = errorBuffer(centroidPARCELA, errorMsg)
QgsProject.instance().addMapLayer(errosApresentacaoDocumentosSimNULL_Parcelas)
errosApresentacaoDocumentosSimNULL_Parcelas.setName(errorMsg)
errosParcelas+=[errosApresentacaoDocumentosSimNULL_Parcelas]

## CODIGO PC & CODIGO PC ID1
query = '("CODIGO_PC" is NULL and "CODIGO_PC_ID1" is NULL)'
centroidPARCELA.selectByExpression(query)

errorMsg = "'Parcela com campos CODIGO_PC e CODIGO_PC_ID1 NULL'"

errosApresentacaoDocumentos_Parcelas = errorBuffer(centroidPARCELA, errorMsg)
QgsProject.instance().addMapLayer(errosApresentacaoDocumentos_Parcelas)
errosApresentacaoDocumentos_Parcelas.setName(errorMsg)
errosParcelas+=[errosApresentacaoDocumentos_Parcelas]

