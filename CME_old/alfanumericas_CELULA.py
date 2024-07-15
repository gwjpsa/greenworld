## work around para fazer import da biblioteca das funções :/
#exec(open('D:/OneDriveGW/PROJECTOS/CME_ARM/scripts/greenWorldPyQgis.py').read())

deleteTemporaryLayers()

### CELULA ###
layerCelula = QgsProject.instance().mapLayersByName('VRCELULA')[0]
entidade = 'Célula'
errosCelulas = []

## OBSERVAÇÕES
field = 'OBSERVACOES'
oldAttribute = "'-'"
newAttribute = 'NULL'
autoFieldCalculator(layerCelula, field, oldAttribute, newAttribute)

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

errosSitExistente = getAttributeErrors(layerCelula, entidade, field, dictSituacaoExistente)

errosCelulas+=errosSitExistente

layerCelula.setSubsetString('"SITUACAO_EXISTENTE" = 1 OR "SITUACAO_EXISTENTE" = 2')

## DESIGNACAO
field = 'DESIGNACAO_CELULA'
dictDesignacao_CELULA = {
    NULL:"NULL'"
}

errosDesignacao_Celulas = getAttributeErrors(layerCelula, entidade, field, dictDesignacao_CELULA)

errosCelulas+=errosDesignacao_Celulas

## ESTADO DE CICLO DE VIDA
field = 'ESTADO_DE_CICLO_DE_VIDA'
dictEstadoCicloVida_CELULA = {
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

errosEstadoCicloVida_Celulas = getAttributeErrors(layerCelula, entidade, field, dictEstadoCicloVida_CELULA)

errosCelulas+=errosEstadoCicloVida_Celulas

## PROPRIETARIO
field = 'PROPRIETARIO'
dictProprietario_CELULA = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosProprietario_Celulas = getAttributeErrors(layerCelula, entidade, field, dictProprietario_CELULA)

errosCelulas+=errosProprietario_Celulas

## TIPO_ACESSO
field = 'TIPO_ACESSO'
dictTipoAcesso_CELULA = {
    0:"\"--Não conhecido--\"'",
    1:"\"Indefinido\"'",
    NULL:"NULL'"
}

errosTipoAcesso_Celulas = getAttributeErrors(layerCelula, entidade, field, dictTipoAcesso_CELULA)

errosCelulas+=errosTipoAcesso_Celulas

## ENTIDADE_GESTORA
field = 'ENTIDADE_GESTORA'
dictEntidadeGestora_CELULA = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosEntidadeGestora_Celulas = getAttributeErrors(layerCelula, entidade, field, dictEntidadeGestora_CELULA)

errosCelulas+=errosEntidadeGestora_Celulas

## MODO_DE_IMPLANTACAO
field = 'MODO_DE_IMPLANTACAO'
dictModoImplantacao_CELULA = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosModoImplantacao_Celulas = getAttributeErrors(layerCelula, entidade, field, dictModoImplantacao_CELULA)

errosCelulas+=errosModoImplantacao_Celulas

## MODO_IDENTIFICACAO
field = 'MODO_IDENTIFICACAO'
dictModoIdentificacao_CELULA = {
    0:"\"--Não conhecido--\"'",
    1:"\"Indefinido\"'",
    NULL:"NULL'"
}

errosModoIdentificacao_Celulas = getAttributeErrors(layerCelula, entidade, field, dictModoIdentificacao_CELULA)

errosCelulas+=errosModoIdentificacao_Celulas

## TIPO_CONSTRUCAO
field = 'TIPO_CONSTRUCAO'
dictTipoConstrucao_CELULA = {
    0:"\"--Não conhecido--\"'",
    9:"\"Indefinido\"'",
    NULL:"NULL'"
}

errosTipoConstrucao_Celulas = getAttributeErrors(layerCelula, entidade, field, dictTipoConstrucao_CELULA)

errosCelulas+=errosTipoConstrucao_Celulas

## TIPO_COBERTURA
field = 'TIPO_COBERTURA'
dictTipoCobertura_CELULA = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosTipoCobertura_Celulas = getAttributeErrors(layerCelula, entidade, field, dictTipoCobertura_CELULA)

errosCelulas+=errosTipoCobertura_Celulas

## TIPO_RESGUARDO
field = 'TIPO_RESGUARDO'
dictTipoResguardo_CELULA = {
    0:"\"--Não conhecido--\"'",
#    1:"\"Indefinido\"'",
    NULL:"NULL'"
}

errosTipoResguardo_Celulas = getAttributeErrors(layerCelula, entidade, field, dictTipoResguardo_CELULA)

errosCelulas+=errosTipoResguardo_Celulas

## MEDICAO_NIVEL
field = 'MEDICAO_NIVEL'
dictMedicaoNivel_CELULA = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosMedicaoNivel_Celulas = getAttributeErrors(layerCelula, entidade, field, dictMedicaoNivel_CELULA)

errosCelulas+=errosMedicaoNivel_Celulas

## TIPO_VEDACAO_RECINTO
field = 'TIPO_VEDACAO_RECINTO'
dictTipoVedacaoRecinto_CELULA = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosTipoVedacaoRecinto_Celulas = getAttributeErrors(layerCelula, entidade, field, dictTipoVedacaoRecinto_CELULA)

errosCelulas+=errosTipoVedacaoRecinto_Celulas

## CONSERVACAO
field = 'CONSERVACAO'
dictConservacao_CELULA = {
    0:"\"--Não conhecido--\"'",
    4:"\"Não Aplicável\"'",
    NULL:"NULL'"
}

errosConservacao_Celulas = getAttributeErrors(layerCelula, entidade, field, dictConservacao_CELULA)

errosCelulas+=errosConservacao_Celulas

## CONSERVACAO_RESGUARDO
field = 'CONSERVACAO_RESGUARDO'
dictConservacaoResguardo_CELULA = {
    0:"\"--Não conhecido--\"'",
    4:"\"Não Aplicável\"'",
    NULL:"NULL'"
}

errosConservacaoResguardo_Celulas = getAttributeErrors(layerCelula, entidade, field, dictConservacaoResguardo_CELULA)

errosCelulas+=errosConservacaoResguardo_Celulas

## NUMERO_ENTRADA
field = 'NUMERO_ENTRADA'
dictNumeroEntradas_CELULA = {
    NULL:"NULL'"
}

errosNumeroEntradas_Celulas = getAttributeErrors(layerCelula, entidade, field, dictNumeroEntradas_CELULA)

errosCelulas+=errosNumeroEntradas_Celulas

## NUMERO_SAIDA
field = 'NUMERO_SAIDA'
dictNumeroSaidas_CELULA = {
    NULL:"NULL'"
}

errosNumeroSaidas_Celulas = getAttributeErrors(layerCelula, entidade, field, dictNumeroSaidas_CELULA)

errosCelulas+=errosNumeroSaidas_Celulas

## FORMA_EM_PLANTA
field = 'FORMA_EM_PLANTA'
dictFormaPlanta_CELULA = {
    0:"\"--Não conhecido--\"'",
    8:"\"Indefinido\"'",
    NULL:"NULL'"
}

errosFormaPlanta_Celulas = getAttributeErrors(layerCelula, entidade, field, dictFormaPlanta_CELULA)

errosCelulas+=errosFormaPlanta_Celulas

## OBSERVAÇÕES
field = 'OBSERVACOES'
oldAttribute = "'-'"
newAttribute = 'NULL'
autoFieldCalculator(layerCelula, field, oldAttribute, newAttribute)