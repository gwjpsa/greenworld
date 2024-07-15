## work around para fazer import da biblioteca das funções :/
#exec(open('D:/OneDriveGW/PROJECTOS/CME_ARM/scripts/greenWorldPyQgis.py').read())

deleteTemporaryLayers()

### VALVULA COMPORTA ###
layerValvulaComporta = QgsProject.instance().mapLayersByName('VRVALVULACOMPORTA')[0]
entidade = 'Válvula Comporta'
errosValvulaComportas = []

## OBSERVAÇÕES
field = 'OBSERVACOES'
oldAttribute = "'-'"
newAttribute = 'NULL'
autoFieldCalculator(layerValvulaComporta, field, oldAttribute, newAttribute)

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

errosSitExistente = getAttributeErrors(layerValvulaComporta, entidade, field, dictSituacaoExistente)

errosValvulaComportas+=errosSitExistente

layerValvulaComporta.setSubsetString('"SITUACAO_EXISTENTE" = 1 OR "SITUACAO_EXISTENTE" = 2')

## TIPO_DE_VALVULA
field = 'TIPO_DE_VALVULA'
dictTipoValvula_VALVULACOMPORTA = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosTipoValvula_ValvulaComportas = getAttributeErrors(layerValvulaComporta, entidade, field, dictTipoValvula_VALVULACOMPORTA)

errosValvulaComportas+=errosTipoValvula_ValvulaComportas

## FUNCAO ????????

## ESTADO DE CICLO DE VIDA
field = 'ESTADO_DE_CICLO_DE_VIDA'
dictEstadoCicloVida_VALVULACOMPORTA = {
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

errosEstadoCicloVida_ValvulaComportas = getAttributeErrors(layerValvulaComporta, entidade, field, dictEstadoCicloVida_VALVULACOMPORTA)

errosValvulaComportas+=errosEstadoCicloVida_ValvulaComportas

## FONTE_DE_INFORMAÇÃO
field = 'FONTE_DE_INFORMACAO'
dictFonteInformacao_VALVULACOMPORTA = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosFonteInformacao_ValvulaComportas = getAttributeErrors(layerValvulaComporta, entidade, field, dictFonteInformacao_VALVULACOMPORTA)

errosValvulaComportas+=errosFonteInformacao_ValvulaComportas

## TIPO_DE_MONTAGEM
field = 'TIPO_DE_MONTAGEM'
dictTipoMontagem_VALVULACOMPORTA = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosTipoMontagem_ValvulaComportas = getAttributeErrors(layerValvulaComporta, entidade, field, dictTipoMontagem_VALVULACOMPORTA)

errosValvulaComportas+=errosTipoMontagem_ValvulaComportas

## MODO_DE_OPERACAO
field = 'MODO_DE_OPERACAO'
dictModoOperacao_VALVULACOMPORTA = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosModoOperacao_ValvulaComportas = getAttributeErrors(layerValvulaComporta, entidade, field, dictModoOperacao_VALVULACOMPORTA)

errosValvulaComportas+=errosModoOperacao_ValvulaComportas

## COLOCACAO
field = 'COLOCACAO'
dictColocacao_VALVULACOMPORTA = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosColocacao_ValvulaComportas = getAttributeErrors(layerValvulaComporta, entidade, field, dictColocacao_VALVULACOMPORTA)

errosValvulaComportas+=errosColocacao_ValvulaComportas

## ESTADO_OPERACIONAL
field = 'ESTADO_OPERACIONAL'
dictEstadoOperacional_VALVULACOMPORTA = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosEstadoOperacional_ValvulaComportas = getAttributeErrors(layerValvulaComporta, entidade, field, dictEstadoOperacional_VALVULACOMPORTA)

errosValvulaComportas+=errosEstadoOperacional_ValvulaComportas

## CONSERVACAO
field = 'CONSERVACAO'
dictConservacao_VALVULACOMPORTA = {
    0:"\"--Não conhecido--\"'",
    4:"\"Não Aplicável\"'",
    NULL:"NULL'"
}

errosConservacao_ValvulaComportas = getAttributeErrors(layerValvulaComporta, entidade, field, dictConservacao_VALVULACOMPORTA)

errosValvulaComportas+=errosConservacao_ValvulaComportas

## PROPRIETARIO
field = 'PROPRIETARIO'
dictProprietario_VALVULACOMPORTA = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosProprietario_ValvulaComportas = getAttributeErrors(layerValvulaComporta, entidade, field, dictProprietario_VALVULACOMPORTA)

errosValvulaComportas+=errosProprietario_ValvulaComportas

## ENTIDADE_GESTORA
field = 'ENTIDADE_GESTORA'
dictEntidadeGestora_VALVULACOMPORTA = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosEntidadeGestora_ValvulaComportas = getAttributeErrors(layerValvulaComporta, entidade, field, dictEntidadeGestora_VALVULACOMPORTA)

errosValvulaComportas+=errosEntidadeGestora_ValvulaComportas

## DIAMETRO_NOMINAL ## Está correto????
field = 'DIAMETRO_NOMINAL'
dictDiametroNominal_VALVULACOMPORTA = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosDiametroNominal_ValvulaComportas = getAttributeErrors(layerValvulaComporta, entidade, field, dictDiametroNominal_VALVULACOMPORTA)

errosValvulaComportas+=errosDiametroNominal_ValvulaComportas

## FABRICANTE ## Está correto????
field = 'FABRICANTE'
dictFabricante_VALVULACOMPORTA = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosFabricante_ValvulaComportas = getAttributeErrors(layerValvulaComporta, entidade, field, dictFabricante_VALVULACOMPORTA)

errosValvulaComportas+=errosFabricante_ValvulaComportas

## MARCA_MOTOR ## Está correto????
field = 'MARCA_MOTOR'
dictMarcaMotor_VALVULACOMPORTA = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosMarcaMotor_ValvulaComportas = getAttributeErrors(layerValvulaComporta, entidade, field, dictMarcaMotor_VALVULACOMPORTA)

errosValvulaComportas+=errosMarcaMotor_ValvulaComportas

## MODELO_VALVULA ## Está correto????
field = 'MODELO_VALVULA'
dictModeloValvula_VALVULACOMPORTA = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosModeloValvula_ValvulaComportas = getAttributeErrors(layerValvulaComporta, entidade, field, dictModeloValvula_VALVULACOMPORTA)

errosValvulaComportas+=errosModeloValvula_ValvulaComportas

## PRESSAO_NOMINAL__BAR ## Está correto????
field = 'PRESSAO_NOMINAL__BAR'
dictPressaoNominalBar_VALVULACOMPORTA = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosPressaoNominalBar_ValvulaComportas = getAttributeErrors(layerValvulaComporta, entidade, field, dictPressaoNominalBar_VALVULACOMPORTA)

errosValvulaComportas+=errosPressaoNominalBar_ValvulaComportas

## VALVULA_ABERTA ## Está correto????
field = 'VALVULA_ABERTA'
dictValvulaAberta_VALVULACOMPORTA = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosValvulaAberta_ValvulaComportas = getAttributeErrors(layerValvulaComporta, entidade, field, dictValvulaAberta_VALVULACOMPORTA)

errosValvulaComportas+=errosValvulaAberta_ValvulaComportas

## NUMERO_DE_SERIE_M ## Está correto????
field = 'NUMERO_DE_SERIE_M'
dictNumSerieMotor_VALVULACOMPORTA = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosNumSerieMotor_ValvulaComportas = getAttributeErrors(layerValvulaComporta, entidade, field, dictNumSerieMotor_VALVULACOMPORTA)

errosValvulaComportas+=errosNumSerieMotor_ValvulaComportas

## NUMERO_SERIE ## Está correto????
field = 'NUMERO_SERIE'
dictNumSerie_VALVULACOMPORTA = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosNumSerie_ValvulaComportas = getAttributeErrors(layerValvulaComporta, entidade, field, dictNumSerie_VALVULACOMPORTA)

errosValvulaComportas+=errosNumSerie_ValvulaComportas

## POTENCIA_MOTOR ## Está correto????
field = 'POTENCIA_MOTOR'
dictPotenciaMotor_VALVULACOMPORTA = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosPotenciaMotor_ValvulaComportas = getAttributeErrors(layerValvulaComporta, entidade, field, dictPotenciaMotor_VALVULACOMPORTA)

errosValvulaComportas+=errosPotenciaMotor_ValvulaComportas

## OBSERVAÇÕES
field = 'OBSERVACOES'
oldAttribute = "'-'"
newAttribute = 'NULL'
autoFieldCalculator(layerValvulaComporta, field, oldAttribute, newAttribute)