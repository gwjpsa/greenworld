## work around para fazer import da biblioteca das funções :/
#exec(open('D:/OneDriveGW/PROJECTOS/CME_ARM/scripts/greenWorldPyQgis.py').read())

deleteTemporaryLayers()

### RESERVATORIO ###
layerReservatorio = QgsProject.instance().mapLayersByName('VRRESERVATORIO')[0]
entidade = 'Reservatório'
errosReservatorios = []

## OBSERVAÇÕES
field = 'OBSERVACOES'
oldAttribute = "'-'"
newAttribute = 'NULL'
autoFieldCalculator(layerReservatorio, field, oldAttribute, newAttribute)

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

errosSitExistente = getAttributeErrors(layerReservatorio, entidade, field, dictSituacaoExistente)

errosReservatorios+=errosSitExistente

layerReservatorio.setSubsetString('"SITUACAO_EXISTENTE" = 1 OR "SITUACAO_EXISTENTE" = 2')

## DESIGNACAO
field = 'DESIGNACAO_EDIFICIO'
dictDesignacao_RESERVATORIO = {
    NULL:"NULL'"
}

errosDesignacao_Reservatorios = getAttributeErrors(layerReservatorio, entidade, field, dictDesignacao_RESERVATORIO)

errosReservatorios+=errosDesignacao_Reservatorios

## ESTADO DE CICLO DE VIDA
field = 'ESTADO_DE_CICLO_DE_VIDA'
dictEstadoCicloVida_RESERVATORIO = {
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

errosEstadoCicloVida_Reservatorios = getAttributeErrors(layerReservatorio, entidade, field, dictEstadoCicloVida_RESERVATORIO)

errosReservatorios+=errosEstadoCicloVida_Reservatorios

## TIPO_ACESSO
field = 'TIPO_ACESSO'
dictTipoAcesso_RESERVATORIO = {
    0:"\"--Não conhecido--\"'",
    1:"\"Indefinido\"'",
    NULL:"NULL'"
}

errosTipoAcesso_Reservatorios = getAttributeErrors(layerReservatorio, entidade, field, dictTipoAcesso_RESERVATORIO)

errosReservatorios+=errosTipoAcesso_Reservatorios

## TIPO_FECHADURA
field = 'TIPO_FECHADURA'
dictTipoFechadura_RESERVATORIO = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosTipoFechadura_Reservatorios = getAttributeErrors(layerReservatorio, entidade, field, dictTipoFechadura_RESERVATORIO)

errosReservatorios+=errosTipoFechadura_Reservatorios

## TIPO_VEDACAO
field = 'TIPO_VEDACAO'
dictTipoVedacao_RESERVATORIO = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosTipoVedacao_Reservatorios = getAttributeErrors(layerReservatorio, entidade, field, dictTipoVedacao_RESERVATORIO)

errosReservatorios+=errosTipoVedacao_Reservatorios

## CONSERVACAO
field = 'CONSERVACAO'
dictConservacao_RESERVATORIO = {
    0:"\"--Não conhecido--\"'",
    4:"\"Não Aplicável\"'",
    NULL:"NULL'"
}

errosConservacao_Reservatorios = getAttributeErrors(layerReservatorio, entidade, field, dictConservacao_RESERVATORIO)

errosReservatorios+=errosConservacao_Reservatorios

## CONSERVACAO_RESGUARDO
field = 'CONSERVACAO_RESGUARDO'
dictConservacaoResguardo_RESERVATORIO = {
    0:"\"--Não conhecido--\"'",
    4:"\"Não Aplicável\"'",
    NULL:"NULL'"
}

errosConservacaoResguardo_Reservatorios = getAttributeErrors(layerReservatorio, entidade, field, dictConservacaoResguardo_RESERVATORIO)

errosReservatorios+=errosConservacaoResguardo_Reservatorios

## PROPRIETARIO
field = 'PROPRIETARIO'
dictProprietario_RESERVATORIO = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosProprietario_Reservatorios = getAttributeErrors(layerReservatorio, entidade, field, dictProprietario_RESERVATORIO)

errosReservatorios+=errosProprietario_Reservatorios

## FONTE_DE_INFORMAÇÃO
field = 'FONTE_DE_INFORMACAO'
dictFonteInformacao_RESERVATORIO = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosFonteInformacao_Reservatorios = getAttributeErrors(layerReservatorio, entidade, field, dictFonteInformacao_RESERVATORIO)

errosReservatorios+=errosFonteInformacao_Reservatorios

## MEDICAO_ENTRADA
field = 'MEDICAO_ENTRADA'
dictMedicaoEntrada_RESERVATORIO = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosMedicaoEntrada_Reservatorios = getAttributeErrors(layerReservatorio, entidade, field, dictMedicaoEntrada_RESERVATORIO)

errosReservatorios+=errosMedicaoEntrada_Reservatorios

## MEDICAO_SAIDA
field = 'MEDICAO_SAIDA'
dictMedicaoSaida_RESERVATORIO = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosMedicaoSaida_Reservatorios = getAttributeErrors(layerReservatorio, entidade, field, dictMedicaoSaida_RESERVATORIO)

errosReservatorios+=errosMedicaoSaida_Reservatorios

## INSTALACAO_ELETRICA
field = 'INSTALACAO_ELETRICA'
dictInstalacaoEletrica_RESERVATORIO = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosInstalacaoEletrica_Reservatorios = getAttributeErrors(layerReservatorio, entidade, field, dictInstalacaoEletrica_RESERVATORIO)

errosReservatorios+=errosInstalacaoEletrica_Reservatorios

## CONTADOR_ENERGIA
field = 'CONTADOR_ENERGIA'
dictContadorEnergia_RESERVATORIO = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosContadorEnergia_Reservatorios = getAttributeErrors(layerReservatorio, entidade, field, dictContadorEnergia_RESERVATORIO)

errosReservatorios+=errosContadorEnergia_Reservatorios

## DETECCAO_INUNDACAO
field = 'DETECCAO_INUNDACAO'
dictDeteccaoInundacao_RESERVATORIO = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosDeteccaoInundacao_Reservatorios = getAttributeErrors(layerReservatorio, entidade, field, dictDeteccaoInundacao_RESERVATORIO)

errosReservatorios+=errosDeteccaoInundacao_Reservatorios

## DETECCAO_INCENDIO
field = 'DETECCAO_INCENDIO'
dictDeteccaoIncendio_RESERVATORIO = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosDeteccaoIncendio_Reservatorios = getAttributeErrors(layerReservatorio, entidade, field, dictDeteccaoIncendio_RESERVATORIO)

errosReservatorios+=errosDeteccaoIncendio_Reservatorios

## DETECCAO_INTRUSAO
field = 'DETECCAO_INTRUSAO'
dictDeteccaoIntrusao_RESERVATORIO = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosDeteccaoIntrusao_Reservatorios = getAttributeErrors(layerReservatorio, entidade, field, dictDeteccaoIntrusao_RESERVATORIO)

errosReservatorios+=errosDeteccaoIntrusao_Reservatorios

## CAMARA_MANOBRAS
field = 'CAMARA_MANOBRAS'
dictCamaraManobras_RESERVATORIO = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosCamaraManobras_Reservatorios = getAttributeErrors(layerReservatorio, entidade, field, dictCamaraManobras_RESERVATORIO)

errosReservatorios+=errosCamaraManobras_Reservatorios

## NUMERO_CELULAS
field = 'NUMERO_CELULAS'
dictNumeroCelulas_RESERVATORIO = {
    NULL:"NULL'"
}

errosNumeroCelulas_Reservatorios = getAttributeErrors(layerReservatorio, entidade, field, dictNumeroCelulas_RESERVATORIO)

errosReservatorios+=errosNumeroCelulas_Reservatorios

## VENTILACAO
field = 'VENTILACAO'
dictVentilacao_RESERVATORIO = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosVentilacao_Reservatorios = getAttributeErrors(layerReservatorio, entidade, field, dictVentilacao_RESERVATORIO)

errosReservatorios+=errosVentilacao_Reservatorios

## REDE_INTERNA
field = 'REDE_INTERNA'
dictRedeInterna_RESERVATORIO = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosRedeInterna_Reservatorios = getAttributeErrors(layerReservatorio, entidade, field, dictRedeInterna_RESERVATORIO)

errosReservatorios+=errosRedeInterna_Reservatorios

## ENTIDADE_GESTORA
field = 'ENTIDADE_GESTORA'
dictEntidadeGestora_RESERVATORIO = {
    0:"\"--Não conhecido--\"'",
    NULL:"NULL'"
}

errosEntidadeGestora_Reservatorios = getAttributeErrors(layerReservatorio, entidade, field, dictEntidadeGestora_RESERVATORIO)

errosReservatorios+=errosEntidadeGestora_Reservatorios

## ALTURA_VEDACAO
field = 'ALTURA_VEDACAO'
dictAlturaVedacao_RESERVATORIO = {
    NULL:"NULL'"
}

errosAlturaVedacao_Reservatorios = getAttributeErrors(layerReservatorio, entidade, field, dictAlturaVedacao_RESERVATORIO)

errosReservatorios+=errosAlturaVedacao_Reservatorios

## Foto1
field = 'FOTO1'
dictFoto1_RESERVATORIO = {
    NULL:"NULL'"
}

errosFoto1_Reservatorios = getAttributeErrors(layerReservatorio, entidade, field, dictFoto1_RESERVATORIO)

errosReservatorios+=errosFoto1_Reservatorios

## Foto2
field = 'FOTO2'
dictFoto2_RESERVATORIO = {
    NULL:"NULL'"
}

errosFoto2_Reservatorios = getAttributeErrors(layerReservatorio, entidade, field, dictFoto2_RESERVATORIO)

errosReservatorios+=errosFoto2_Reservatorios

## OBSERVAÇÕES
field = 'OBSERVACOES'
oldAttribute = "'-'"
newAttribute = 'NULL'
autoFieldCalculator(layerReservatorio, field, oldAttribute, newAttribute)