## work around para fazer import da biblioteca das funções :/
#exec(open('D:/OneDriveGW/PROJECTOS/CME_ARM/scripts/greenWorldPyQgis.py').read())

deleteTemporaryLayers()

### CANAL ###
layerCanal = QgsProject.instance().mapLayersByName('VRCANAL')[0]
entidade = 'Canal'
errosCanais = []

## OBSERVAÇÕES
field = 'OBSERVACOES'
oldAttribute = "'-'"
newAttribute = 'NULL'
autoFieldCalculator(layerCanal, field, oldAttribute, newAttribute)

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

errosSitExistente = getAttributeErrors(layerCanal, entidade, field, dictSituacaoExistente)

errosCanais+=errosSitExistente

layerCanal.setSubsetString('"SITUACAO_EXISTENTE" = 1 OR "SITUACAO_EXISTENTE" = 2')

## ESTADO DE CICLO DE VIDA
field = 'ESTADO_DE_CICLO_DE_VIDA'
dictEstadoCicloVida_CANAL = {
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

errosEstadoCicloVida_Canais = getAttributeErrors(layerCanal, entidade, field, dictEstadoCicloVida_CANAL)

errosCanais+=errosEstadoCicloVida_Canais

## TIPO ACESSO
field = 'TIPO_ACESSO'
dictTipoAcesso_CANAL = {
    0:"\"--Não conhecido--\"'",
    1:"\"Indefinido\"'",
    NULL:"NULL'"
}

errosTipoAcesso_Canais = getAttributeErrors(layerCanal, entidade, field, dictTipoAcesso_CANAL)

errosCanais+=errosTipoAcesso_Canais

## CONSERVACAO
field = 'CONSERVACAO'
dictConservacao_CANAL = {
    0:"\"--Não conhecido--\"'",
    4:"\"Não Aplicável\"'",
    NULL:"NULL'"
}

errosConservacao_Canais = getAttributeErrors(layerCanal, entidade, field, dictConservacao_CANAL)

errosCanais+=errosConservacao_Canais

## CAPACIDADE
field = 'CAPACIDADE_REGADEIRAS'
dictCapacidade_CANAL = {
    NULL:"NULL'"
}

errosCapacidade_Canais = getAttributeErrors(layerCanal, entidade, field, dictCapacidade_CANAL)

errosCanais+=errosCapacidade_Canais

## PROPRIETARIO
field = 'PROPRIETARIO'
dictProprietario_CANAL = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosProprietario_Canais = getAttributeErrors(layerCanal, entidade, field, dictProprietario_CANAL)

errosCanais+=errosProprietario_Canais

## MODO_IDENTIFICACAO
field = 'MODO_IDENTIFICACAO'
dictModoIdentificacao_CANAL = {
    0:"\"--Não conhecido--\"'",
    1:"\"Indefinido\"'",
    NULL:"NULL'"
}

errosModoIdentificacao_Canais = getAttributeErrors(layerCanal, entidade, field, dictModoIdentificacao_CANAL)

errosCanais+=errosModoIdentificacao_Canais

## TIPO_DE_INFRASTRUTURA
field = 'TIPO_DE_INFRASTRUTURA'
dictTipoInfraestrutura_CANAL = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosTipoInfraestrutura_Canais = getAttributeErrors(layerCanal, entidade, field, dictTipoInfraestrutura_CANAL)

errosCanais+=errosModoIdentificacao_Canais

## TIPO_DE_ASSENTAMENTO
field = 'TIPO_DE_ASSENTAMENTO'
dictTipoAssentamento_CANAL = {
    0:"\"--Não conhecido--\"'",
    1:"\"Indefinido\"'",
    NULL:"NULL'"
}

errosTipoAssentamento_Canais = getAttributeErrors(layerCanal, entidade, field, dictTipoAssentamento_CANAL)

errosCanais+=errosTipoAssentamento_Canais

## MATERIAL
field = 'MATERIAL_CANAL'
dictMaterial_CANAL = {
    0:"\"--Não conhecido--\"'",
    1:"\"Indefinido\"'",
    NULL:"NULL'"
}

errosMaterial_Canais = getAttributeErrors(layerCanal, entidade, field, dictMaterial_CANAL)

errosCanais+=errosMaterial_Canais


## DIMENSÕES TUBAGENS

dictMaterial_diametro_CANAL = {
    3:"\"Tubo PEAD\"'",
    4:"\"Tubo PVC\"'",
    5:"\"Tubo Galvanizado\"'",
    7:"\"Manilha de Betão\"'",
    11:"\"Ferro Fundido\"'"
}

dictMaterial_larguraAltura_CANAL = {
    2:"\"Betão a céu aberto\"'",
    6:"\"Terra Batida\"'",
    8:"\"Pré-fabricado\"'",
    9:"\"Calçada\"'",
    10:"\"Pedra\"'",
    12:"\"Outro Material\"'",
    13:"\"Betão\"'"
}

## DIAMETRO_TUBAGENS
field = 'DIAMETRO_TUBAGENS'
oldAttr = NULL
newAttr = '0'
autoFieldCalculator(layerCanal, field, oldAttr, newAttr)

errosDiametroCanais = []

for k in dictMaterial_diametro_CANAL.keys():
    auxExpression = '"{}" = 0 AND "MATERIAL_CANAL" = {}'.format(field, k)
    layerCanal.selectByExpression(auxExpression)
    errorMsg = "'Canal com campo DIAMETRO_TUBAGENS = 0 e MATERIAL_CANAL {}".format(dictMaterial_diametro_CANAL[k])
    layerErrors = errorBuffer(layerCanal, errorMsg)
    if layerErrors.featureCount() > 0:
        print('ola')
        errosDiametroCanais.append(layerErrors)
        QgsProject.instance().addMapLayer(errosDiametroCanais[-1])
        errosDiametroCanais[-1].setName(errorMsg)


for k in dictMaterial_larguraAltura_CANAL.keys():
    auxExpression = '"{}" != 0 AND "MATERIAL_CANAL" = {}'.format(field, k)
    layerCanal.selectByExpression(auxExpression)
    errorMsg = "'Canal com campo DIAMETRO_TUBAGENS != 0 e MATERIAL_CANAL {}".format(dictMaterial_larguraAltura_CANAL[k])
    layerErrors = errorBuffer(layerCanal, errorMsg)
    if layerErrors.featureCount() > 0:
        errosDiametroCanais.append(layerErrors)
        QgsProject.instance().addMapLayer(errosDiametroCanais[-1])
        errosDiametroCanais[-1].setName(errorMsg)

errosCanais+=errosDiametroCanais

## LARGURA_MEDIA
field = 'LARGURA_MEDIA'
oldAttr = NULL
newAttr = '0'
autoFieldCalculator(layerCanal, field, oldAttr, newAttr)

errosLarguraCanais = []

for k in dictMaterial_diametro_CANAL.keys():
    auxExpression = '"{}" != 0 AND "MATERIAL_CANAL" = {}'.format(field, k)
    layerCanal.selectByExpression(auxExpression)
    errorMsg = "'Canal com campo LARGURA_MEDIA = 0 e MATERIAL_CANAL {}".format(dictMaterial_diametro_CANAL[k])
    layerErrors = errorBuffer(layerCanal, errorMsg)
    if layerErrors.featureCount() > 0:
        print('ola')
        errosLarguraCanais.append(layerErrors)
        QgsProject.instance().addMapLayer(errosLarguraCanais[-1])
        errosLarguraCanais[-1].setName(errorMsg)

for k in dictMaterial_larguraAltura_CANAL.keys():
    auxExpression = '"{}" = 0 AND "MATERIAL_CANAL" = {}'.format(field, k)
    layerCanal.selectByExpression(auxExpression)
    errorMsg = "'Canal com campo LARGURA_MEDIA != 0 e MATERIAL_CANAL {}".format(dictMaterial_larguraAltura_CANAL[k])
    layerErrors = errorBuffer(layerCanal, errorMsg)
    if layerErrors.featureCount() > 0:
        errosLarguraCanais.append(layerErrors)
        QgsProject.instance().addMapLayer(errosLarguraCanais[-1])
        errosLarguraCanais[-1].setName(errorMsg)
 
errosCanais+=errosLarguraCanais
 
## ALTURA_MEDIA
field = 'ALTURA_MEDIA'
oldAttr = NULL
newAttr = '0'
autoFieldCalculator(layerCanal, field, oldAttr, newAttr)

errosAlturaCanais = []

for k in dictMaterial_diametro_CANAL.keys():
    auxExpression = '"{}" != 0 AND "MATERIAL_CANAL" = {}'.format(field, k)
    layerCanal.selectByExpression(auxExpression)
    errorMsg = "'Canal com campo ALTURA_MEDIA = 0 e MATERIAL_CANAL {}".format(dictMaterial_diametro_CANAL[k])
    layerErrors = errorBuffer(layerCanal, errorMsg)
    if layerErrors.featureCount() > 0:
        print('ola')
        errosAlturaCanais.append(layerErrors)
        QgsProject.instance().addMapLayer(errosAlturaCanais[-1])
        errosAlturaCanais[-1].setName(errorMsg)

for k in dictMaterial_larguraAltura_CANAL.keys():
    auxExpression = '"{}" = 0 AND "MATERIAL_CANAL" = {}'.format(field, k)
    layerCanal.selectByExpression(auxExpression)
    errorMsg = "'Canal com campo ALTURA_MEDIA != 0 e MATERIAL_CANAL {}".format(dictMaterial_larguraAltura_CANAL[k])
    layerErrors = errorBuffer(layerCanal, errorMsg)
    if layerErrors.featureCount() > 0:
        errosAlturaCanais.append(layerErrors)
        QgsProject.instance().addMapLayer(errosAlturaCanais[-1])
        errosAlturaCanais[-1].setName(errorMsg)

errosCanais+=errosAlturaCanais

## OBSERVAÇÕES
field = 'OBSERVACOES'
layerCanal.selectByExpression(('"{}" = ' + "'-'").format(field))
if len(layerCanal.selectedFeatures()) > 0:
    layerCanal.startEditing()
    NULL2ZERO = QgsExpression('NULL')
    for f in layerCanal.selectedFeatures():
        context = QgsExpressionContext()
        context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layerCanal))
        context.setFeature(f)
        f[field] = NULL2ZERO.evaluate(context)
        layerCanal.updateFeature(f)
    layerCanal.commitChanges()