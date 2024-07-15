## GreenWorld QGis Python
from email.message import EmailMessage
import ssl
import smtplib
### NÃO EDITAR FUNÇÕES

def errorBuffer(errorFeatures, errorMsg, dist = 1.5, numSeg = 5):
    """
    Esta função faz buffers a partir de uma lista de features
    por defeito, o buffer é "circular, com raio de 1.5m
    ao buffer é atribuída uma mensagem (string) associada, 
    que corresponde ao erro que se está a assinalar
    """
    errorBufferLayer = processing.run("native:buffer", {
        'INPUT':QgsProcessingFeatureSourceDefinition(errorFeatures.source(), selectedFeaturesOnly=True),
        'DISTANCE':dist,
        'SEGMENTS':numSeg,
        'END_CAP_STYLE':0,
        'JOIN_STYLE':0,
        'MITER_LIMIT':2,
        'DISSOLVE':False,
        'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT
    })['OUTPUT']
    
    deletedFields = []
    i = 0
    for field in errorBufferLayer.fields():
        if i == 0:
            pass
        else:
            deletedFields.append(i)
        i+=1

    errorBufferLayer.startEditing()
    errorBufferLayer.dataProvider().deleteAttributes(deletedFields)
    errorBufferLayer.dataProvider().addAttributes([QgsField('ID', QVariant.Int), QgsField('Duvidas_Gabinete', QVariant.String), QgsField('Resposta_Campo', QVariant.String)])
    errorBufferLayer.updateFields()

    errorBufferLayer.selectAll()
    expression = QgsExpression(errorMsg)
    ## expression = QgsExpression("'ola'") # teste

    for f in errorBufferLayer.selectedFeatures():
        context = QgsExpressionContext()
        context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(errorBufferLayer))
        context.setFeature(f)
        f['Duvidas_Gabinete'] = expression.evaluate(context)
        errorBufferLayer.updateFeature(f)

    errorBufferLayer.commitChanges()
    
    return(errorBufferLayer)
    
def createWKTField(layer, fieldName = 'wkt', expressionQGis = 'geom_to_wkt($geometry)'):
    """
    Esta função cria um campo (por defeito - "wkt") na layer indicada;
    as features são preenchidas através da expressão expressionQGis (field calculator)
    'geom_to_wkt($geometry)'
    """
    layer.selectAll()
    layer.startEditing()
    pr = layer.dataProvider()
    pr.addAttributes([QgsField(fieldName, QVariant.String)])
    layer.updateFields()

    expression = QgsExpression(expressionQGis)

    for f in layer.selectedFeatures():
        context = QgsExpressionContext()
        context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer))
        context.setFeature(f)
        f[fieldName] = expression.evaluate(context)
        layer.updateFeature(f)
    layer.commitChanges()

def getUniqueAndDuplicated(lista):
    """
    Esta função devolve duas listas:
        1. uma lista com os unique elements a lista original
        2. uma lista com os elementos que estão duplicados na lista original
    """
    unique = []
    duplicate = []
    for elem in lista:
        if elem not in unique:
            unique.append(elem)
        else:
            duplicate.append(elem)
    
    return(unique, duplicate)

def createJoin(joinLayer, targetLayer, idJoinLayer="ID1", idTargetLayer="ID1", joinLayerFields=["wkt"]):
    """
    Esta função cria um join entre duas layers, com base nos campos indicados (por defeito "ID1").
    Por defeito, é adicionada à targetLayer o campo wkt da joinLayer.
    """
    targetLayer.startEditing()
    joinObjectCaixa=QgsVectorLayerJoinInfo()
    joinObjectCaixa.setJoinFieldName(idJoinLayer)
    joinObjectCaixa.setTargetFieldName(idTargetLayer)
    joinObjectCaixa.setJoinLayerId(joinLayer.id())
    joinObjectCaixa.setJoinFieldNamesSubset(joinLayerFields)
    joinObjectCaixa.setUsingMemoryCache(True)
    joinObjectCaixa.setJoinLayer(joinLayer)
    targetLayer.addJoin(joinObjectCaixa)
    targetLayer.commitChanges()

def updateGeometryFromWKT(layer, wktGeometryAttributeIndex = -1):
    """
    Esta função atualiza a geometria das features da layer pretendida,
    com base no último atributo da lista de atributos (por defeito, ou seja index = -1)
    """
    layer.startEditing()
    for f in layer.getFeatures():
        wktGeom = f.attributes()[wktGeometryAttributeIndex]
        try:
            layer.changeGeometry(f.id(),QgsGeometry.fromWkt(wktGeom))
        except:
            pass
    layer.commitChanges()

def deleteTemporaryLayers(QgsProj = QgsProject.instance()):
    """
    Esta função remove/elimina todas as layers temporárias do Qgs.
    Usualmente utilizada no início do programa na fase de desenvolvimento/teste,
    para eliminar os produtos da iteração anterior.
    """
    layers = QgsProj.mapLayers()
    for layer_id, layer in layers.items():
        if 'memory?' in layer.dataProvider().dataSourceUri() or 'processing_cxMtHN' in layer.dataProvider().dataSourceUri():
            # print(layer.name())
            QgsProj.removeMapLayer(QgsProj.mapLayersByName(layer.name())[0].id())

def getAttributeErrors(layer, entidade, field, dictKeyValues):
    
    fieldInitQuery = '"{}" = '.format(field)

    initErrorMsg = "'{} com campo {} preenchido com ".format(entidade, field)
    
    listErrorLayers = []
    for k in dictKeyValues.keys():
        if k != NULL:
            expression = fieldInitQuery + str(k)
        else:
            expression = '"{}" is {}'.format(field, k)
            initErrorMsg = "'{} com campo {} ".format(entidade, field)
            
        expression = expression + ' AND "OBSERVACOES" is NULL'
        
        layer.selectByExpression(expression)
        
        errorMsg = initErrorMsg + dictKeyValues[k]
        
        layerErrors = errorBuffer(layer, errorMsg)
        if layerErrors.featureCount()> 0:
            listErrorLayers.append(layerErrors)
            QgsProject.instance().addMapLayer(listErrorLayers[-1])
            listErrorLayers[-1].setName(errorMsg)
    return(listErrorLayers)

def autoFieldCalculator(layer, field, oldAttribute, newAttribute):
    if oldAttribute == NULL:
        layer.selectByExpression(('"{}" is NULL').format(field))
    else:
        layer.selectByExpression(('"{}" = {}').format(field, oldAttribute))
    if len(layer.selectedFeatures()) > 0:
        layer.startEditing()
        expression = QgsExpression(newAttribute)
        for f in layer.selectedFeatures():
            context = QgsExpressionContext()
            context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer))
            context.setFeature(f)
            f[field] = expression.evaluate(context)
            layer.updateFeature(f)
        layer.commitChanges()

def sendNotificationMail(
    subject,
    body,
    emailSmtp = 'smtp.gmail.com',
    port = 465,
    sender = 'sig.greenworld@gmail.com',
    pwd = 'glnmgaqjezivcuay',
    receiver = ['rhcsilva@gmail.com', 'jooaosa@gmail.com']
    ):
    
    """
    por defeito, sender = sig.greenworld@gmail.combinations
    receivers: Ricardo e João
    """
    
    email_sender = sender
    email_pwd = pwd
    email_receiver = receiver

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', port, context = context) as smtp:
        smtp.login(email_sender, email_pwd)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
        
    print('Email enviado com sucesso!')

def createDuplicateLayer(layer, geometry, crs_epsg = 3061, name = "duplicate_layer"):
    feats = [feat for feat in layer.getFeatures()]

    mem_layer = QgsVectorLayer("{}?crs=epsg:{}".format(geometry, crs_epsg), name, "memory")

    mem_layer_data = mem_layer.dataProvider()
    attr = layer.dataProvider().fields().toList()
    mem_layer_data.addAttributes(attr)
    mem_layer.updateFields()
    mem_layer_data.addFeatures(feats)

    QgsProject.instance().addMapLayer(mem_layer)
    return(mem_layer)

def exportRaster(file_out_name, file_out_full_path, layer):
    file_writer = QgsRasterFileWriter(file_out_full_path)
    pipe = QgsRasterPipe()
    provider = layer.dataProvider()

    if not pipe.set(provider.clone()):
        print("Cannot set pipe provider")
        pass

    file_writer.writeRaster(
        pipe,
        provider.xSize(),
        provider.ySize(),
        provider.extent(),
        provider.crs()
    )

print('GW Python Lib foi importada')