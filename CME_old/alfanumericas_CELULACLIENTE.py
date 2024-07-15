## work around para fazer import da biblioteca das funções :/
#exec(open('D:/OneDriveGW/PROJECTOS/CME_ARM/scripts/greenWorldPyQgis.py').read())

deleteTemporaryLayers()

### CELULA CLIENTE ###
layerCelulaCliente = QgsProject.instance().mapLayersByName('VRCELULACLIENTE')[0]
entidade = 'Célula Cliente'
errosCelulaCliente = []

## OBSERVAÇÕES
field = 'OBSERVACOES'
oldAttribute = "'-'"
newAttribute = 'NULL'
autoFieldCalculator(layerCelulaCliente, field, oldAttribute, newAttribute)

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

errosSitExistente = getAttributeErrors(layerCelulaCliente, entidade, field, dictSituacaoExistente)

errosCelulaCliente+=errosSitExistente

layerCelulaCliente.setSubsetString('"SITUACAO_EXISTENTE" = 1 OR "SITUACAO_EXISTENTE" = 2')

## ESTADO DE CICLO DE VIDA
field = 'ESTADO_DE_CICLO_DE_VIDA'
dictEstadoCicloVida_CELULACLIENTE = {
    0:"\"--Não conhecido--\"'",
    6:"\"Desativado\"'",
    8:"\"Indicativo\"'",
    9:"\"Desligado/Reserva\"'",
    10:"\"Tem condições de funcionamento\"'",
    11:"\"Recuperável com algum investimento\"'",
    12:"\"Sem condicoes de recuperação\"'",
    15:"\"Indefinido\"'",
    16:"\"Manutencao\"'",
    NULL:"NULL'"
}

errosEstadoCicloVida_CelulaCliente = getAttributeErrors(layerCelulaCliente, entidade, field, dictEstadoCicloVida_CELULACLIENTE)

errosCelulaCliente+=errosEstadoCicloVida_CelulaCliente

## FONTE INFORMAÇÃO
field = 'FONTE_DE_INFORMACAO'
dictFonteInformacao_CELULACLIENTE = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosFonteInformacao_CelulaCliente = getAttributeErrors(layerCelulaCliente, entidade, field, dictFonteInformacao_CELULACLIENTE)

errosCelulaCliente+=errosFonteInformacao_CelulaCliente

## MODO_IDENTIFICACAO
field = 'MODO_IDENTIFICACAO'
dictModoIdentificacao_CELULACLIENTE = {
    0:"\"--Não conhecido--\"'",
    1:"\"Indefinido\"'",
    NULL:"NULL'"
}

errosModoIdentificacao_CelulaCliente = getAttributeErrors(layerCelulaCliente, entidade, field, dictModoIdentificacao_CELULACLIENTE)

errosCelulaCliente+=errosModoIdentificacao_CelulaCliente

## CONSERVACAO
field = 'ESTADO_CONSERVACAO'
dictConservacao_CELULACLIENTE = {
    0:"\"--Não conhecido--\"'",
    4:"\"Não Aplicável\"'",
    NULL:"NULL'"
}

errosConservacao_CelulaCliente = getAttributeErrors(layerCelulaCliente, entidade, field, dictConservacao_CELULACLIENTE)

errosCelulaCliente+=errosConservacao_CelulaCliente

## TIPO VEDACAO
field = 'TIPO_VEDACAO_RECINTO'
dictConservacao_CELULACLIENTE = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosConservacao_CelulaCliente = getAttributeErrors(layerCelulaCliente, entidade, field, dictConservacao_CELULACLIENTE)

errosCelulaCliente+=errosConservacao_CelulaCliente

## ENTIDADE GESTORA
field = 'ENTIDADE_GESTORA'
dictEntidadeGestora_CELULACLIENTE = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosEntidadeGestora_CelulaCliente = getAttributeErrors(layerCelulaCliente, entidade, field, dictEntidadeGestora_CELULACLIENTE)

errosCelulaCliente+=errosEntidadeGestora_CelulaCliente

## DESIGNACAO_CELULA_CLIENTE
field = 'DESIGNACAO_CELULA_CLIENTE'
oldAttribute = "'-'"
newAttribute = 'NULL'
autoFieldCalculator(layerCelulaCliente, field, oldAttribute, newAttribute)

## OBSERVAÇÕES
field = 'OBSERVACOES'
oldAttribute = "'-'"
newAttribute = 'NULL'
autoFieldCalculator(layerCelulaCliente, field, oldAttribute, newAttribute)

## Merge duvidas numa única layer

#duvidasCelulaCliente = processing.run("native:mergevectorlayers", {
#    'LAYERS':errosCelulaCliente,
#    'CRS':None,
#    'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
#})['OUTPUT']
#
#deleteTemporaryLayers()
#
#QgsProject.instance().addMapLayer(duvidasCelulaCliente)
#duvidasCelulaCliente.setName('duvidasCelulaCliente')
#