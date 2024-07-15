strAuxCommunes = 'D:/___DEEPFACES_SERVER/zar3i_site_updates/{}/3_communesV/zstats'.format(dir_update)
strAuxNDVI = 'D:/___DEEPFACES_SERVER/zar3i_site_updates/{}/2_merge/NDVI.tif'.format(dir_update)
strAuxNDMI = 'D:/___DEEPFACES_SERVER/zar3i_site_updates/{}/2_merge/NDMI.tif'.format(dir_update)

merged = processing.run("native:mergevectorlayers",{
    'LAYERS':[
        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'0274-0340\'.gpkg',
        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'0341-0390\'.gpkg',
        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'0391-0440\'.gpkg',
        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'0441-0490\'.gpkg',
        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'0491-0540\'.gpkg',
        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'0541-0590\'.gpkg',
        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'0591-0640\'.gpkg',
        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'0641-0690\'.gpkg',
        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'0691-0740\'.gpkg',
        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'0741-0790\'.gpkg',
        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'0791-0840\'.gpkg',
        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'0841-0890\'.gpkg',
        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'0891-0940\'.gpkg',
        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'0941-0990\'.gpkg',
        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'0991-1040\'.gpkg',
        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'1041-1090\'.gpkg',
        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'1091-1152\'.gpkg'
    ],
#    'LAYERS':[
#        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'0274-0340\'.gpkg|layername=communes_zonalStats_NDMI_NDVI_\'0274-0340\'',
#        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'0341-0390\'.gpkg|layername=communes_zonalStats_NDMI_NDVI_\'0341-0390\'',
#        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'0391-0440\'.gpkg|layername=communes_zonalStats_NDMI_NDVI_\'0391-0440\'',
#        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'0441-0490\'.gpkg|layername=communes_zonalStats_NDMI_NDVI_\'0441-0490\'',
#        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'0491-0540\'.gpkg|layername=communes_zonalStats_NDMI_NDVI_\'0491-0540\'',
#        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'0541-0590\'.gpkg|layername=communes_zonalStats_NDMI_NDVI_\'0541-0590\'',
#        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'0591-0640\'.gpkg|layername=communes_zonalStats_NDMI_NDVI_\'0591-0640\'',
#        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'0641-0690\'.gpkg|layername=communes_zonalStats_NDMI_NDVI_\'0641-0690\'',
#        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'0691-0740\'.gpkg|layername=communes_zonalStats_NDMI_NDVI_\'0691-0740\'',
#        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'0741-0790\'.gpkg|layername=communes_zonalStats_NDMI_NDVI_\'0741-0790\'',
#        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'0791-0840\'.gpkg|layername=communes_zonalStats_NDMI_NDVI_\'0791-0840\'',
#        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'0841-0890\'.gpkg|layername=communes_zonalStats_NDMI_NDVI_\'0841-0890\'',
#        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'0891-0940\'.gpkg|layername=communes_zonalStats_NDMI_NDVI_\'0891-0940\'',
#        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'0941-0990\'.gpkg|layername=communes_zonalStats_NDMI_NDVI_\'0941-0990\'',
#        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'0991-1040\'.gpkg|layername=communes_zonalStats_NDMI_NDVI_\'0991-1040\'',
#        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'1041-1090\'.gpkg|layername=communes_zonalStats_NDMI_NDVI_\'1041-1090\'',
#        strAuxCommunes+'/communes_zonalStats_NDMI_NDVI_\'1091-1152\'.gpkg|layername=communes_zonalStats_NDMI_NDVI_\'1091-1152\''
#    ],
    'CRS':None,
    'OUTPUT':'D:/___DEEPFACES_SERVER/zar3i_site_updates/{}/3_communesV/zstats/zstats_final.gpkg'.format(dir_update)
})['OUTPUT']
#QgsProject.instance().addMapLayer(merged)

tablename = 'agriculture_field'
geometrycol = "geometry"

from qgis.core import QgsVectorLayer, QgsDataSourceUri

for tenant in tenants:
    print(tenant)
    uri = QgsDataSourceUri()
    uri.setConnection('165.227.135.116', '5432', 'ayishi', 'developer', 'ObuEm8Ap')
    tablename = 'agriculture_field'
    uri.setDataSource (tenant, tablename, geometrycol)
    tenant_fields=QgsVectorLayer (uri.uri(), tablename, "postgres")
    QgsProject.instance().addMapLayer(tenant_fields)

    tenant_zstats_ndvi=processing.run("native:zonalstatisticsfb", {
        'INPUT':tenant_fields,
        'INPUT_RASTER':strAuxNDVI,
        'RASTER_BAND':1,
        'COLUMN_PREFIX':'ndvi_',
        'STATISTICS':[2],
        'OUTPUT':'TEMPORARY_OUTPUT'
    })['OUTPUT']

    tenant_zstats=processing.run("native:zonalstatisticsfb", {
        'INPUT':tenant_zstats_ndvi,
        'INPUT_RASTER':strAuxNDMI,
        'RASTER_BAND':1,
        'COLUMN_PREFIX':'ndmi_',
        'STATISTICS':[2],
        'OUTPUT':'D:/___DEEPFACES_SERVER/zar3i_site_updates/{}/3_communesV/zstats/zstats_FIELDS_{}.gpkg'.format(dir_update,tenant)
    })['OUTPUT']
    tenant_zstats_layer = QgsVectorLayer(tenant_zstats, tenant, "ogr")
    QgsProject.instance().addMapLayer(tenant_zstats_layer)
    tenant_zstats_layer.setName('zstats_FIELDS_{}'.format(tenant))
    
    del tenant_zstats
    del tenant_zstats_layer
