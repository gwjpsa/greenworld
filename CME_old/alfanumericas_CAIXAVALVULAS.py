## work around para fazer import da biblioteca das funções :/
#exec(open('D:/OneDriveGW/PROJECTOS/CME_ARM/scripts/greenWorldPyQgis.py').read())

deleteTemporaryLayers()

### CAIXA VALVULAS ###
layerCaixaValvulas = QgsProject.instance().mapLayersByName('VRCAIXAVALVULAS')[0]
entidade = 'Caixa de Válvulas'
errosCaixaValvulas = []

## OBSERVAÇÕES
field = 'OBSERVACOES'
oldAttribute = "'-'"
newAttribute = 'NULL'
autoFieldCalculator(layerCaixaValvulas, field, oldAttribute, newAttribute)

## DESIGNAÇÃO
field = 'DESIGNACAO'
oldAttribute = "'-'"
newAttribute = 'NULL'
autoFieldCalculator(layerCaixaValvulas, field, oldAttribute, newAttribute)

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

errosSitExistente = getAttributeErrors(layerCaixaValvulas, entidade, field, dictSituacaoExistente)

errosCaixaValvulas+=errosSitExistente

layerCaixaValvulas.setSubsetString('"SITUACAO_EXISTENTE" = 1 OR "SITUACAO_EXISTENTE" = 2')

## FUNCAO_DE_CAIXA
field = 'FUNCAO_DE_CAIXA'
dictFuncaoCaixa_CAIXAVALVULAS = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosFuncaoCaixa_CaixaValvulas = getAttributeErrors(layerCaixaValvulas, entidade, field, dictFuncaoCaixa_CAIXAVALVULAS)

errosCaixaValvulas+=errosFuncaoCaixa_CaixaValvulas

## ESTADO DE CICLO DE VIDA
field = 'ESTADO_DE_CICLO_DE_VIDA'
dictEstadoCicloVida_CAIXAVALVULAS = {
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

errosEstadoCicloVida_CaixaValvulas = getAttributeErrors(layerCaixaValvulas, entidade, field, dictEstadoCicloVida_CAIXAVALVULAS)

errosCaixaValvulas+=errosEstadoCicloVida_CaixaValvulas

## TIPO_ACESSO
field = 'TIPO_ACESSO'
dictTipoAcesso_CAIXAVALVULAS = {
    0:"\"--Não conhecido--\"'",
    1:"\"Indefinido\"'",
    NULL:"NULL'"
}

errosTipoAcesso_CaixaValvulas = getAttributeErrors(layerCaixaValvulas, entidade, field, dictTipoAcesso_CAIXAVALVULAS)

errosCaixaValvulas+=errosTipoAcesso_CaixaValvulas

## TIPO_ENTRADA
field = 'TIPO_ENTRADA'
dictTipoEntrada_CAIXAVALVULAS = {
    0:"\"--Não conhecido--\"'",
    3:"\"NC\"'",
    NULL:"NULL'"
}

errosTipoEntrada_CaixaValvulas = getAttributeErrors(layerCaixaValvulas, entidade, field, dictTipoEntrada_CAIXAVALVULAS)

errosCaixaValvulas+=errosTipoEntrada_CaixaValvulas

## DIMENSAO_CAIXA
field = 'DIMENSAO_CAIXA'
dictDimensaoCaixa_CAIXAVALVULAS = {
    NULL:"NULL'"
}

errosDimensaoCaixa_CaixaValvulas = getAttributeErrors(layerCaixaValvulas, entidade, field, dictDimensaoCaixa_CAIXAVALVULAS)

errosCaixaValvulas+=errosDimensaoCaixa_CaixaValvulas

## DIMENSAO_TAMPA
field = 'DIMENSAO_TAMPA'
dictDimensaoTampa_CAIXAVALVULAS = {
    NULL:"NULL'"
}

errosDimensaoTampa_CaixaValvulas = getAttributeErrors(layerCaixaValvulas, entidade, field, dictDimensaoTampa_CAIXAVALVULAS)

errosCaixaValvulas+=errosDimensaoTampa_CaixaValvulas

## FORMA_TAMPA
field = 'FORMA_TAMPA'
dictFormaTampa_CAIXAVALVULAS = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosFormaTampa_CaixaValvulas = getAttributeErrors(layerCaixaValvulas, entidade, field, dictFormaTampa_CAIXAVALVULAS)

errosCaixaValvulas+=errosFormaTampa_CaixaValvulas

## MATERIAL
field = 'MATERIAL'
dictMaterial_CAIXAVALVULAS = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosMaterial_CaixaValvulas = getAttributeErrors(layerCaixaValvulas, entidade, field, dictMaterial_CAIXAVALVULAS)

errosCaixaValvulas+=errosMaterial_CaixaValvulas

## MATERIAL_TAMPA
field = 'MATERIAL_TAMPA'
dictMaterialTampa_CAIXAVALVULAS = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosMaterialTampa_CaixaValvulas = getAttributeErrors(layerCaixaValvulas, entidade, field, dictMaterialTampa_CAIXAVALVULAS)

errosCaixaValvulas+=errosMaterialTampa_CaixaValvulas

## CONSERVACAO
field = 'CONSERVACAO'
dictConservacao_CAIXAVALVULAS = {
    0:"\"--Não conhecido--\"'",
    4:"\"Não Aplicável\"'",
    NULL:"NULL'"
}

errosConservacao_CaixaValvulas = getAttributeErrors(layerCaixaValvulas, entidade, field, dictConservacao_CAIXAVALVULAS)

errosCaixaValvulas+=errosConservacao_CaixaValvulas

## FORMA_EM_PLANTA
field = 'FORMA_EM_PLANTA'
dictFormaPlanta_CAIXAVALVULAS = {
    0:"\"--Não conhecido--\"'",
    8:"\"Indefinido\"'",
    NULL:"NULL'"
}

errosFormaPlanta_CaixaValvulas = getAttributeErrors(layerCaixaValvulas, entidade, field, dictFormaPlanta_CAIXAVALVULAS)

errosCaixaValvulas+=errosFormaPlanta_CaixaValvulas

## PROPRIETARIO
field = 'PROPRIETARIO'
dictProprietario_CAIXAVALVULAS = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosProprietario_CaixaValvulas = getAttributeErrors(layerCaixaValvulas, entidade, field, dictProprietario_CAIXAVALVULAS)

errosCaixaValvulas+=errosProprietario_CaixaValvulas

## MODO_IDENTIFICACAO
field = 'MODO_IDENTIFICACAO'
dictModoIdentificacao_CAIXAVALVULAS = {
    0:"\"--Não conhecido--\"'",
    1:"\"Indefinido\"'",
    NULL:"NULL'"
}

errosModoIdentificacao_CaixaValvulas = getAttributeErrors(layerCaixaValvulas, entidade, field, dictModoIdentificacao_CAIXAVALVULAS)

errosCaixaValvulas+=errosModoIdentificacao_CaixaValvulas

## MODO_DE_IMPLANTACAO
field = 'MODO_DE_IMPLANTACAO'
dictModoImplantacao_CAIXAVALVULAS = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosModoImplantacao_CaixaValvulas = getAttributeErrors(layerCaixaValvulas, entidade, field, dictModoImplantacao_CAIXAVALVULAS)

errosCaixaValvulas+=errosModoImplantacao_CaixaValvulas

## ALTURA_UTIL
field = 'ALTURA_UTIL'
dictAlturaUtil_CAIXAVALVULAS = {
    NULL:"NULL'"
}

errosAlturaUtil_CaixaValvulas = getAttributeErrors(layerCaixaValvulas, entidade, field, dictAlturaUtil_CAIXAVALVULAS)

errosCaixaValvulas+=errosAlturaUtil_CaixaValvulas

## INSCRICAO_TAMPA
field = 'INSCRICAO_TAMPA'
dictInscricaoTampa_CAIXAVALVULAS = {
    NULL:"NULL'"
}

errosInscricaoTampa_CaixaValvulas = getAttributeErrors(layerCaixaValvulas, entidade, field, dictInscricaoTampa_CAIXAVALVULAS)

errosCaixaValvulas+=errosInscricaoTampa_CaixaValvulas

## OBSERVAÇÕES
field = 'OBSERVACOES'
oldAttribute = "'-'"
newAttribute = 'NULL'
autoFieldCalculator(layerCaixaValvulas, field, oldAttribute, newAttribute)