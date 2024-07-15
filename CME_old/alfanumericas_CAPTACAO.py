## work around para fazer import da biblioteca das funções :/
#exec(open('D:/OneDriveGW/PROJECTOS/CME_ARM/scripts/greenWorldPyQgis.py').read())

deleteTemporaryLayers()

### CAPTACAO ###
layerCaptacao = QgsProject.instance().mapLayersByName('VRCAPTACAO')[0]
entidade = 'Captacao'
errosCaptacao = []

## OBSERVAÇÕES
field = 'OBSERVACOES'
oldAttribute = "'-'"
newAttribute = 'NULL'
autoFieldCalculator(layerCaptacao, field, oldAttribute, newAttribute)

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

errosSitExistente = getAttributeErrors(layerCaptacao, entidade, field, dictSituacaoExistente)

errosCaptacao+=errosSitExistente

layerCaptacao.setSubsetString('"SITUACAO_EXISTENTE" = 1 OR "SITUACAO_EXISTENTE" = 2')

## DESIGNACAO_EDIFICIO
field = 'DESIGNACAO_CAPTACAO'
dictDesignacaoCaptacao_CAPTACAO = {
    NULL:"NULL'"
}

errosDesignacaoCaptacao_Captacao = getAttributeErrors(layerCaptacao, entidade, field, dictDesignacaoCaptacao_CAPTACAO)

errosCaptacao+=errosDesignacaoCaptacao_Captacao

## ESTADO DE CICLO DE VIDA
field = 'ESTADO_DE_CICLO_DE_VIDA'
dictEstadoCicloVida_CAPTACAO = {
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

errosEstadoCicloVida_Captacao = getAttributeErrors(layerCaptacao, entidade, field, dictEstadoCicloVida_CAPTACAO)

errosCaptacao+=errosEstadoCicloVida_Captacao

## CAPTACAO_TIPO
field = 'CAPTACAO_TIPO'
dictCaptacaoTipo_CAPTACAO = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosCaptacaoTipo_Captacao = getAttributeErrors(layerCaptacao, entidade, field, dictCaptacaoTipo_CAPTACAO)

errosCaptacao+=errosCaptacaoTipo_Captacao

## FONTE_DE_INFORMAÇÃO
field = 'FONTE_DE_INFORMACAO'
dictFonteInformacao_CAPTACAO = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosFonteInformacao_Captacao = getAttributeErrors(layerCaptacao, entidade, field, dictFonteInformacao_CAPTACAO)

errosCaptacao+=errosFonteInformacao_Captacao

## MODO_IDENTIFICACAO
field = 'MODO_IDENTIFICACAO'
dictModoIdentificacao_CAPTACAO = {
    0:"\"--Não conhecido--\"'",
    1:"\"Indefinido\"'",
    NULL:"NULL'"
}

errosModoIdentificacao_Captacao = getAttributeErrors(layerCaptacao, entidade, field, dictModoIdentificacao_CAPTACAO)

errosCaptacao+=errosModoIdentificacao_Captacao

## CONSERVACAO
field = 'CONSERVACAO'
dictConservacao_CAPTACAO = {
    0:"\"--Não conhecido--\"'",
    4:"\"Não Aplicável\"'",
    NULL:"NULL'"
}

errosConservacao_Captacao = getAttributeErrors(layerCaptacao, entidade, field, dictConservacao_CAPTACAO)

errosCaptacao+=errosConservacao_Captacao

## Foto1
field = 'FOTO1'
dictFoto1_CAPTACAO = {
    NULL:"NULL'"
}

errosFoto1_Captacao = getAttributeErrors(layerCaptacao, entidade, field, dictFoto1_CAPTACAO)

errosCaptacao+=errosFoto1_Captacao

## Foto2
field = 'FOTO2'
dictFoto2_CAPTACAO = {
    NULL:"NULL'"
}

errosFoto2_Captacao = getAttributeErrors(layerCaptacao, entidade, field, dictFoto2_CAPTACAO)

errosCaptacao+=errosFoto2_Captacao

## OBSERVAÇÕES
field = 'OBSERVACOES'
oldAttribute = "'-'"
newAttribute = 'NULL'
autoFieldCalculator(layerCaptacao, field, oldAttribute, newAttribute)