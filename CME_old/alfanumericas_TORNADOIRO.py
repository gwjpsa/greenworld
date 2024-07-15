## work around para fazer import da biblioteca das funções :/
#exec(open('D:/OneDriveGW/PROJECTOS/CME_ARM/scripts/greenWorldPyQgis.py').read())

deleteTemporaryLayers()

### PARCELA ###
layerTornadoiro = QgsProject.instance().mapLayersByName('VRTORNADOIRO')[0]
entidade = 'Tornadoiro'
errosTornadoiros = []

## OBSERVAÇÕES
field = 'OBSERVACOES'
oldAttribute = "'-'"
newAttribute = 'NULL'
autoFieldCalculator(layerTornadoiro, field, oldAttribute, newAttribute)

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

errosSitExistente = getAttributeErrors(layerTornadoiro, entidade, field, dictSituacaoExistente)

errosTornadoiros+=errosSitExistente

layerTornadoiro.setSubsetString('"SITUACAO_EXISTENTE" = 1 OR "SITUACAO_EXISTENTE" = 2')

## DESTINO_AGUA
field = 'DESTINO_AGUA'
dictDestinoAgua_TORNADOIRO = {
    NULL:"NULL'"
}

errosDestinoAgua_Tornadoiros = getAttributeErrors(layerTornadoiro, entidade, field, dictDestinoAgua_TORNADOIRO)

errosTornadoiros+=errosDestinoAgua_Tornadoiros

## ESTADO_TORNADOIRO
field = 'ESTADO_TORNADOIRO'
dictEstadoTornadoiro_TORNADOIRO = {
    NULL:"NULL'"
}

errosEstadoTornadoiro_Tornadoiros = getAttributeErrors(layerTornadoiro, entidade, field, dictEstadoTornadoiro_TORNADOIRO)

errosTornadoiros+=errosEstadoTornadoiro_Tornadoiros

## CODIGO_CLIENTE_DECLARANTE
field = 'CODIGO_CLIENTE_DECLARANTE'
dictCodClienteDeclarante_TORNADOIRO = {
    NULL:"NULL'"
}

errosCodClienteDeclarante_Tornadoiros = getAttributeErrors(layerTornadoiro, entidade, field, dictCodClienteDeclarante_TORNADOIRO)

errosTornadoiros+=errosCodClienteDeclarante_Tornadoiros

## RELACAO_DECLARANTE_TITULAR
field = 'RELACAO_DECLARANTE_TITULAR'
dictRelacaoDeclaranteTitular_TORNADOIRO = {
    NULL:"NULL'"
}

errosCodClienteDeclarante_Tornadoiros = getAttributeErrors(layerTornadoiro, entidade, field, dictRelacaoDeclaranteTitular_TORNADOIRO)

errosTornadoiros+=errosCodClienteDeclarante_Tornadoiros

## APRESENTACAO_DOCUMENTOS
field = 'APRESENTACAO_DOCUMENTOS'
dictApresentacaoDocumentos_TORNADOIRO = {
    NULL:"NULL'"
}

errosApresentacaoDocumentos_Tornadoiros = getAttributeErrors(layerTornadoiro, entidade, field, dictApresentacaoDocumentos_TORNADOIRO)

errosTornadoiros+=errosApresentacaoDocumentos_Tornadoiros

## CODIGO PC & CODIGO PC ID1
query = '("CODIGO_PC" is NULL and "CODIGO_PC_ID1" is NULL)'
layerTornadoiro.selectByExpression(query)

errorMsg = "'Tornadoiro com campos CODIGO_PC e CODIGO_PC_ID1 NULL'"

errosApresentacaoDocumentos_Tornadoiros = errorBuffer(layerTornadoiro, errorMsg)
QgsProject.instance().addMapLayer(errosApresentacaoDocumentos_Tornadoiros)
errosApresentacaoDocumentos_Tornadoiros.setName(errorMsg)
errosTornadoiros+=[errosApresentacaoDocumentos_Tornadoiros]

## OBSERVAÇÕES
field = 'OBSERVACOES'
oldAttribute = "'-'"
newAttribute = 'NULL'
autoFieldCalculator(layerTornadoiro, field, oldAttribute, newAttribute)