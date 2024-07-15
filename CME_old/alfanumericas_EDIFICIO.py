## work around para fazer import da biblioteca das funções :/
#exec(open('D:/OneDriveGW/PROJECTOS/CME_ARM/scripts/greenWorldPyQgis.py').read())

deleteTemporaryLayers()

### EDIFICIO ###
layerEdificio = QgsProject.instance().mapLayersByName('VCEDIFICIO')[0]
entidade = 'Edificio'
errosEdificios = []

## OBSERVAÇÕES
field = 'OBSERVACOES'
oldAttribute = "'-'"
newAttribute = 'NULL'
autoFieldCalculator(layerEdificio, field, oldAttribute, newAttribute)

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

errosSitExistente = getAttributeErrors(layerEdificio, entidade, field, dictSituacaoExistente)

errosEdificios+=errosSitExistente

layerEdificio.setSubsetString('"SITUACAO_EXISTENTE" = 1 OR "SITUACAO_EXISTENTE" = 2')

## DESIGNACAO_EDIFICIO
field = 'DESIGNACAO_EDIFICIO'
dictDesignacaoEdificio_EDIFICIO = {
    NULL:"NULL'"
}

errosDesignacaoEdificio_Edificios = getAttributeErrors(layerEdificio, entidade, field, dictDesignacaoEdificio_EDIFICIO)

errosEdificios+=errosDesignacaoEdificio_Edificios

## FUNCAO_EDIFICIO
field = 'FUNCAO_EDIFICIO'
dictFuncaoEdificio_EDIFICIO = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosFuncaoEdificio_Edificios = getAttributeErrors(layerEdificio, entidade, field, dictFuncaoEdificio_EDIFICIO)

errosEdificios+=errosFuncaoEdificio_Edificios

## ESTADO DE CICLO DE VIDA
field = 'ESTADO_DE_CICLO_DE_VIDA'
dictEstadoCicloVida_EDIFICIO = {
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

errosEstadoCicloVida_Edificios = getAttributeErrors(layerEdificio, entidade, field, dictEstadoCicloVida_EDIFICIO)

errosEdificios+=errosEstadoCicloVida_Edificios

## CONSERVACAO
field = 'CONSERVACAO'
dictConservacao_EDIFICIO = {
    0:"\"--Não conhecido--\"'",
    4:"\"Não Aplicável\"'",
    NULL:"NULL'"
}

errosConservacao_Edificios = getAttributeErrors(layerEdificio, entidade, field, dictConservacao_EDIFICIO)

errosEdificios+=errosConservacao_Edificios

## NUMERO_DE_COZINHAS
field = 'NUMERO_DE_COZINHAS'
dictNumCozinhas_EDIFICIO = {
    NULL:"NULL'"
}

errosNumCozinhas_Edificios = getAttributeErrors(layerEdificio, entidade, field, dictNumCozinhas_EDIFICIO)

errosEdificios+=errosNumCozinhas_Edificios

## NUMERO_DE_PISOS
field = 'NUMERO_DE_PISOS'
dictNumPisos_EDIFICIO = {
    NULL:"NULL'"
}

errosNumPisos_Edificios = getAttributeErrors(layerEdificio, entidade, field, dictNumPisos_EDIFICIO)

errosEdificios+=errosNumPisos_Edificios

## NUMERO_DE_QUARTOS
field = 'NUMERO_DE_QUARTOS'
dictNumQuartos_EDIFICIO = {
    NULL:"NULL'"
}

errosNumQuartos_Edificios = getAttributeErrors(layerEdificio, entidade, field, dictNumQuartos_EDIFICIO)

errosEdificios+=errosNumQuartos_Edificios

## NUMERO_DE_WC
field = 'NUMERO_DE_WC'
dictNumWC_EDIFICIO = {
    NULL:"NULL'"
}

errosNumWC_Edificios = getAttributeErrors(layerEdificio, entidade, field, dictNumWC_EDIFICIO)

errosEdificios+=errosNumWC_Edificios

## Foto1
field = 'FOTO1'
dictFoto1_EDIFICIO = {
    NULL:"NULL'"
}

errosFoto1_Edificios = getAttributeErrors(layerEdificio, entidade, field, dictFoto1_EDIFICIO)

errosEdificios+=errosFoto1_Edificios

## Foto2
field = 'FOTO2'
dictFoto2_EDIFICIO = {
    NULL:"NULL'"
}

errosFoto2_Edificios = getAttributeErrors(layerEdificio, entidade, field, dictFoto2_EDIFICIO)

errosEdificios+=errosFoto2_Edificios

## OBSERVAÇÕES
field = 'OBSERVACOES'
oldAttribute = "'-'"
newAttribute = 'NULL'
autoFieldCalculator(layerEdificio, field, oldAttribute, newAttribute)