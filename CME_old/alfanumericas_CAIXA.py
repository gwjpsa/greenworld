## work around para fazer import da biblioteca das funções :/
#exec(open('D:/OneDriveGW/PROJECTOS/CME_ARM/scripts/greenWorldPyQgis.py').read())

#deleteTemporaryLayers()

### CAIXA ###
layerCaixa = QgsProject.instance().mapLayersByName('VRCAIXA')[0]
entidade = 'Caixa'
errosCaixas = []

## OBSERVAÇÕES
field = 'OBSERVACOES'
oldAttribute = "'-'"
newAttribute = 'NULL'
autoFieldCalculator(layerCaixa, field, oldAttribute, newAttribute)

field = 'OBSERVACOES'
oldAttribute = "' '"
newAttribute = 'NULL'
autoFieldCalculator(layerCaixa, field, oldAttribute, newAttribute)

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

errosSitExistente = getAttributeErrors(layerCaixa, entidade, field, dictSituacaoExistente)

errosCaixas+=errosSitExistente

#layerCaixa.setSubsetString('"SITUACAO_EXISTENTE" = 1 OR "SITUACAO_EXISTENTE" = 2')

## FUNCAO CAIXA
field = 'FUNCAO_DE_CAIXA'
dictFuncaoCaixa_CAIXA = {
    0:"\"--Não conhecido--\"'",
    1:"\"Indefinido\"'",
    NULL:"NULL'"
}

errosFuncaoCaixa_Caixas = getAttributeErrors(layerCaixa, entidade, field, dictFuncaoCaixa_CAIXA)

errosCaixas+=errosFuncaoCaixa_Caixas

## TIPO DE OPERAÇÃO
field = 'TIPO_OPERACAO'
dictTipoOperacao_CAIXA = {
    0:"\"--Não conhecido--\"'",
    1:"\"Indefinido\"'",
    2:"\"NA (Não Aplicável)\"'",
    NULL:"NULL'"
}

errosTipoOperacao_Caixas = getAttributeErrors(layerCaixa, entidade, field, dictTipoOperacao_CAIXA)

errosCaixas+=errosTipoOperacao_Caixas

## ESTADO DE CICLO DE VIDA
field = 'ESTADO_DE_CICLO_DE_VIDA'
dictEstadoCicloVida_CAIXA = {
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

errosEstadoCicloVida_Caixas = getAttributeErrors(layerCaixa, entidade, field, dictEstadoCicloVida_CAIXA)

errosCaixas+=errosEstadoCicloVida_Caixas

## TIPO ACESSO
field = 'TIPO_ACESSO'
dictTipoAcesso_CAIXA = {
    0:"\"--Não conhecido--\"'",
    1:"\"Indefinido\"'",
    NULL:"NULL'"
}

errosTipoAcesso_Caixas = getAttributeErrors(layerCaixa, entidade, field, dictTipoAcesso_CAIXA)

errosCaixas+=errosTipoAcesso_Caixas

## CONSERVACAO
field = 'ESTADO_CONSERVA'
dictConservacao_CAIXA = {
    0:"\"--Não conhecido--\"'",
    4:"\"Não Aplicável\"'",
    NULL:"NULL'"
}

errosConservacao_Caixas = getAttributeErrors(layerCaixa, entidade, field, dictConservacao_CAIXA)

errosCaixas+=dictConservacao_CAIXA

## CAPACIDADE
field = 'CAPACIDADE_REGADEIRAS'
dictCapacidade_CAIXA = {
    NULL:"NULL'"
}

errosCapacidade_Caixas = getAttributeErrors(layerCaixa, entidade, field, dictCapacidade_CAIXA)

errosCaixas+=errosCapacidade_Caixas

## PROPRIETARIO
field = 'PROPRIETARIO'
dictProprietario_CAIXA = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosProprietario_Caixas = getAttributeErrors(layerCaixa, entidade, field, dictProprietario_CAIXA)

errosCaixas+=errosProprietario_Caixas

## MODO_IDENTIFICACAO
field = 'MODO_IDENTIFICACAO'
dictModoIdentificacao_CAIXA = {
    0:"\"--Não conhecido--\"'",
    1:"\"Indefinido\"'",
    NULL:"NULL'"
}

errosModoIdentificacao_Caixas = getAttributeErrors(layerCaixa, entidade, field, dictModoIdentificacao_CAIXA)

errosCaixas+=errosModoIdentificacao_Caixas

## COMPRIMENTO
field = 'COMPRIMENTO_CAIXA'
oldAttr = NULL
newAttr = '0'
autoFieldCalculator(layerCaixa, field, oldAttr, newAttr)

### LARGURA
field = 'LARGURA_CAIXA'
oldAttr = NULL
newAttr = '0'
autoFieldCalculator(layerCaixa, field, oldAttr, newAttr)