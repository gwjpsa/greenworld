## work around para fazer import da biblioteca das funções :/
#exec(open('D:/OneDriveGW/PROJECTOS/CME_ARM/scripts/greenWorldPyQgis.py').read())

deleteTemporaryLayers()

### PONTO DE ENTREGA ###
layerPE = QgsProject.instance().mapLayersByName('VRPONTOENTREGA')[0]
entidade = 'Ponto de Entrega'
errosPE = []

## OBSERVAÇÕES
field = 'OBSERVACOES'
oldAttribute = "'-'"
newAttribute = 'NULL'
autoFieldCalculator(layerPE, field, oldAttribute, newAttribute)

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

errosSitExistente = getAttributeErrors(layerPE, entidade, field, dictSituacaoExistente)

errosPE+=errosSitExistente

layerPE.setSubsetString('"SITUACAO_EXISTENTE" = 1 OR "SITUACAO_EXISTENTE" = 2')

## MODO IDENTIFICACAO
field = 'MODO_IDENTIFICACAO'
dictModoIdentificacao_PE = {
    0:"\"--Não conhecido--\"'",
    1:"\"Indefinido\"'",
    NULL:"NULL'"
}

errosModoIdentificacao_PE = getAttributeErrors(layerPE, entidade, field, dictModoIdentificacao_PE)

errosPE+=errosModoIdentificacao_PE

## ESTADO DO PE
field = 'ESTADO_PC'
dictEstado_PE = {
    NULL:"NULL'"
}

errosEstado_PE = getAttributeErrors(layerPE, entidade, field, dictEstado_PE)

errosPE+=errosEstado_PE

## CODIGO CAIXA
field = 'CODIGO_CAIXA'
expression = '"CODIGO_CAIXA" <> ' + "geomintersects('VRCANAL_VRCAIXA','VRCAIXA_CODIGO_CAIXA')"
msgError = "'Ponto de Entrega com CODIGO_CAIXA errado"
layerPE.selectByExpression(expression)

errosCodigoCaixa_PE = errorBuffer(layerPE, msgError)

if errosCodigoCaixa_PE.featureCount()> 0:
    QgsProject.instance().addMapLayer(errosCodigoCaixa_PE)
    errosCodigoCaixa_PE.setName(msgError)
    errosPE+=[errosCodigoCaixa_PE]

## CODIGO CAIXA ID1
field = 'CODIGO_CAIXA'
expression = '"CODIGO_CAIXA_ID1" <> ' + "geomintersects('VRCANAL_VRCAIXA','VRCAIXA_ID1')"
msgError = "'Ponto de Entrega com CODIGO_CAIXA_ID1 errado"
layerPE.selectByExpression(expression)

errosCodigoCaixaID1_PE = errorBuffer(layerPE, msgError)

if errosCodigoCaixaID1_PE.featureCount()> 0:
    QgsProject.instance().addMapLayer(errosCodigoCaixaID1_PE)
    errosCodigoCaixaID1_PE.setName(msgError)
    errosPE+=[errosCodigoCaixaID1_PE]