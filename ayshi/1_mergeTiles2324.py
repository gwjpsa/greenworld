import os

#path_images = f'D:/___DEEPFACES_SERVER/zar3i/zar3i_site/{dir_update}/1_bands/NDVI/'
#output = f'D:/___DEEPFACES_SERVER/zar3i/zar3i_site/{dir_update}/2_merge/'
def mergeTiles(path_images, path_out, aux, name_out):
    list_imgs = os.listdir(path_images)

    list_imgs_r_29 = []
    list_imgs_r_30 = []
    for img in list_imgs:
        if '_30' in img and 'xml' not in img:
            reprojected_30_tiles = processing.run("gdal:warpreproject", {
                'INPUT':path_images + img,
                'SOURCE_CRS':None,
                'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:32629'),
                'RESAMPLING':0,
                'NODATA':None,
                'TARGET_RESOLUTION':None,
                'OPTIONS':'',
                'DATA_TYPE':0,
                'TARGET_EXTENT':None,
                'TARGET_EXTENT_CRS':None,
                'MULTITHREADING':False,
                'EXTRA':'',
                'OUTPUT':aux + img #+ '.tif'
            })['OUTPUT']
            list_imgs_r_29.append(reprojected_30_tiles)
        elif '_29' in img and 'xml' not in img:
            list_imgs_r_29.append(path_images + img)

    mergeTiles_30 = processing.run("gdal:merge", {
        'INPUT':list_imgs_r_29,
        'PCT':False,
        'SEPARATE':False,
        'NODATA_INPUT':0,
        'NODATA_OUTPUT':-9999,
        'OPTIONS':'',
        'EXTRA':'',
        'DATA_TYPE':5,
        'OUTPUT':path_out+name_out
    })['OUTPUT']
    raster_layer_mergeTiles30 = QgsRasterLayer(mergeTiles_30, name_out[:-4])
    QgsProject.instance().addMapLayer(raster_layer_mergeTiles30, True)
    
#    for filename in os.listdir(aux):
#        file_path = os.path.join(aux, filename)
#        try:
#            if os.path.isfile(file_path) or os.path.islink(file_path):
#                os.unlink(file_path)
#            elif os.path.isdir(file_path):
#                shutil.rmtree(file_path)
#        except Exception as e:
#            print('Failed to delete %s. Reason: %s' % (file_path, e))
            
    return(list_imgs_r_29)

aux = f'D:/___DEEPFACES_SERVER/zar3i_site_updates/{dir_update}/2_merge/auxiliar/'
output = f'D:/___DEEPFACES_SERVER/zar3i_site_updates/{dir_update}/2_merge/'

path_images_ndvi = f'D:/___DEEPFACES_SERVER/zar3i_site_updates/{dir_update}/1_bands/NDVI/'
mergeTiles(path_images_ndvi, aux, aux, 'NDVI.tif')

#path_images_ndmi = f'D:/___DEEPFACES_SERVER/zar3i_site_updates/{dir_update}/1_bands/NDMI/'
#mergeTiles(path_images_ndmi, output, aux, 'NDMI.tif')