# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 14:59:33 2023

@author: joaos
"""
#%% IGNORAR
# import os
# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
# from osgeo import gdal
# import numpy

# #os.environ['PROJ_LIB'] = r'C:\Users\joaos\anaconda3_v2\envs\geo\Lib\site-packages\rasterio\proj_data'

# def calcNDVI(nir, red):
#     return(np.nan_to_num((nir - red) / (nir + red)))

# def qualityComposite(original_bands, indices):
#     return(original_bands[indices, np.arange(indices.shape[0])[:, np.newaxis], np.arange(indices.shape[1])])

# def readImage(path):
#     return gdal.Open(path).GetRasterBand(1).ReadAsArray()

# list_tiles = [
#     '29RMQ',
#     '29RNQ',
#     '29RPQ',
#     '29RQQ',
#     '29SMR',
#     '29SMS',
#     '29SNR',
#     '29SNS',
#     '29SNT',
#     '29SPR',
#     '29SPS',
#     '29SPT',
#     '29SQR',
#     '29SQS',
#     '29SQT',
#     '29SQU',
#     '30STA',
#     '30STB',
#     '30STC',
#     '30STD',
#     '30SUA',
#     '30SUB',
#     '30SUC',
#     '30SUD',
#     '30SVB',
#     '30SVC',
#     '30SVD'
# ]

# bands = [
#     'B04',
#     'B08',
#     'B11'
# ]

# file = r'C:\Users\joaos\OneDrive\Ambiente de Trabalho\DF\zar3i\1_bands_teste\B11\T29RMQ_20231001T112121_B11_20m.jp2'
# path = r'C:\Users\joaos\OneDrive\Ambiente de Trabalho\DF\zar3i\1_bands_teste/'
# output = r'C:\Users\joaos\OneDrive\Ambiente de Trabalho\DF\zar3i\1_bands_teste\B11_10m\ola2.tiff'

# images_B04 = os.listdir(path + bands[0])
# images_B08 = os.listdir(path + bands[1])
# images_B11 = os.listdir(path + bands[2])

# for tile in list_tiles:
#     for i, band in enumerate(images_B04[:1]):
        
#         B08_by_tile = []
#         B11_by_tile = []
#         NDVI_by_tile = []
        
#         if tile in band:
#             B08_by_tile.append(readImage(path + 'B08/' + images_B08[i]).GetRasterBand(1).ReadAsArray())
#             B8 = readImage(path + 'B08/' + images_B08[i]).GetRasterBand(1).ReadAsArray()
#             B4 = readImage(path + 'B04/' + images_B04[i]).GetRasterBand(1).ReadAsArray()
#             NDVI_by_tile.append(calcNDVI(B8, B4))

#             B11 = readImage(path + 'B11/' + images_B11[i])
        
#             xres=10
#             yres=10
#             resample_alg = 'near'
            
#             driver = gdal.GetDriverByName('MEM')
#             output_ds = driver.Create('', B11.RasterXSize*2, B11.RasterYSize*2, 1, gdal.GDT_Int16)
#             output_ds.SetGeoTransform(B11.GetGeoTransform())
#             output_ds.SetProjection(B11.GetProjection())
            
#             ds = gdal.Warp(output_ds, B11, xRes=xres, yRes=yres, resampleAlg=resample_alg)
#             ds = None

#             B11_by_tile.append(output_ds.GetRasterBand(1).ReadAsArray())
            
        
#%% EXECUTAR

import os
import numpy as np
from osgeo import gdal, osr

def calcNDVI(nir, red):
    return np.nan_to_num((nir - red) / (nir + red))

def qualityComposite(original_bands, indices):
    return(original_bands[indices, np.arange(indices.shape[0])[:, np.newaxis], np.arange(indices.shape[1])])

def readImage(path):
    dataset = gdal.Open(path)
    band = dataset.GetRasterBand(1)
    array = band.ReadAsArray()
    return dataset, array

def resample_image(input_path, output_path, xres=10, yres=10, resample_alg='bilinear'):
    input_dataset = gdal.Open(input_path)
    if input_dataset is None:
        print("Error: Unable to open the input image.")
        return
    
    input_projection = input_dataset.GetProjection()
    input_geotransform = input_dataset.GetGeoTransform()
    
    if input_geotransform is None:
        print("Error: Unable to retrieve geotransform information.")
        return

    # Calculate output dimensions based on new resolution
    input_cols = input_dataset.RasterXSize
    input_rows = input_dataset.RasterYSize
    
    output_cols = round(input_cols * (input_geotransform[1] / xres))
    output_rows = round(input_rows * (abs(input_geotransform[5]) / yres))

    if output_cols <= 0 or output_rows <= 0:
        print("Error: Invalid output size calculated.")
        return

    output_driver = gdal.GetDriverByName('GTiff')

    # Create a virtual dataset for resampling
    mem_drv = gdal.GetDriverByName('MEM')
    mem_ds = mem_drv.Create('', output_cols, output_rows, 1, gdal.GDT_Float32)
    mem_ds.SetGeoTransform((input_geotransform[0], xres, 0, input_geotransform[3], 0, -yres))
    mem_ds.SetProjection(input_projection)

    # Convert resample_alg to GDALResampleAlg type
    resample_algorithm = getattr(gdal, 'GRA_NearestNeighbour')

    # Perform the resampling
    gdal.ReprojectImage(input_dataset, mem_ds, None, None, resample_algorithm)

    # Create an output dataset and write the resampled data
    output_ds = output_driver.CreateCopy(output_path, mem_ds, 0)
    
def export_array_as_geotiff(array, output_path, geotransform):
    # Get array shape and type
    rows, cols = array.shape
    dtype = array.dtype
    
    # Create the GeoTIFF driver
    driver = gdal.GetDriverByName("GTiff")

    # Create a new GeoTIFF file
    dataset = driver.Create(output_path, cols, rows, 1, gdal.GDT_Float32)

    # Set the geotransform
    dataset.SetGeoTransform(geotransform)

    # Set the projection to EPSG:32629/32630
    srs = osr.SpatialReference()
    if '_30' in output_path:
        srs.ImportFromEPSG(32630)
    else:
        srs.ImportFromEPSG(32629)
    dataset.SetProjection(srs.ExportToWkt())

    # Write the array data into the GeoTIFF
    band = dataset.GetRasterBand(1)
    band.WriteArray(array)

    # Flush data to disk and close dataset
    band.FlushCache()
    dataset.FlushCache()
    dataset = None

list_tiles = [
    '29RMQ',
    '29RNQ',
    '29RPQ',
    '29RQQ',
    '29SMR',
    '29SMS',
    '29SNR',
    '29SNS',
    '29SNT',
    '29SPR',
    '29SPS',
    '29SPT',
    '29SQR',
    '29SQS',
    '29SQT',
    '29SQU',
    '30STA',
    '30STB',
    '30STC',
    '30STD',
    '30SUA',
    '30SUB',
    '30SUC',
    '30SUD',
    '30SVB',
    '30SVC',
    '30SVD'
]

bands = [
    'B04',
    'B08',
    'B11'
]

directory = '202406d'

path = f'D:/___DEEPFACES_SERVER/zar3i_site_updates/{directory}/1_bands/'

images_B04 = os.listdir(path + bands[0])
images_B08 = os.listdir(path + bands[1])
images_B11 = os.listdir(path + bands[2])

images_B04.sort()
images_B08.sort()
images_B11.sort()
#list_tiles = ['29RNQ', '29RMQ', '30SVB', '30SVC', '30SVD']
for tile in list_tiles:
    try:
        print(tile)
        list_ndvi_tile = []
        list_ndmi_tile = []
        for i, image in enumerate(images_B04):
            print(image)
            if tile in image:
                try: 
                    B08_dataset, B08_array = readImage(os.path.join(path, 'B08', images_B08[i]))
                    B04_dataset, B04_array = readImage(os.path.join(path, 'B04', images_B04[i]))
                    
                    NDVI = (calcNDVI(B08_array, B04_array)*10000).astype(np.int16)
                    list_ndvi_tile.append(NDVI)
                    
                    B11_path = path + 'B11/' + images_B11[i]
                    output_path = f'D:/___DEEPFACES_SERVER/zar3i_site_updates/{directory}/1_bands/B11_10_m/{images_B11[i][:-7]}resampled_10m.tif'
                   
                    resample_image(B11_path, output_path)
                    B11_dataset, B11_array = readImage(output_path)
                    
                    NDMI = (calcNDVI(B08_array, B11_array)*10000).astype(np.int16) 
                    list_ndmi_tile.append(NDMI)
                    
                    del B08_array
                    del B04_array
                    del B11_array
                    del NDMI
                    del NDVI
                except:
                    pass
        
        img_NDVI = np.stack(list_ndvi_tile, axis = 0)
        max_indices = np.argmax(img_NDVI, axis=0)
        
        good_NDVI = qualityComposite(img_NDVI, max_indices)
        mask = (good_NDVI/10000 >= -1) & (good_NDVI/10000 <= 1)
        result_NDVI = np.where(mask, good_NDVI/10000, -9999)
        export_array_as_geotiff(result_NDVI.astype(np.float32),  f'D:/___DEEPFACES_SERVER/zar3i_site_updates/{directory}/1_bands/NDVI/NDVI_{tile}.tif', B04_dataset.GetGeoTransform())
        
        good_NDMI = qualityComposite(np.stack(list_ndmi_tile, axis = 0), max_indices)
        mask = (good_NDMI/10000 >= -1) & (good_NDMI/10000 <= 1)
        result_NDMI = np.where(mask, good_NDMI/10000, -9999)    
        export_array_as_geotiff(result_NDMI.astype(np.float32),  f'D:/___DEEPFACES_SERVER/zar3i_site_updates/{directory}/1_bands/NDMI/NDMI_{tile}.tif', B04_dataset.GetGeoTransform())
    except:
        pass


#%% IGNORAR

# import os
# import numpy as np
# from osgeo import gdal, osr

# def calcNDVI(nir, red):
#     return np.nan_to_num((nir - red) / (nir + red))

# def qualityComposite(original_bands, indices):
#     return(original_bands[indices, np.arange(indices.shape[0])[:, np.newaxis], np.arange(indices.shape[1])])

# def readImage(path):
#     dataset = gdal.Open(path)
#     band = dataset.GetRasterBand(1)
#     array = band.ReadAsArray()
#     return dataset, array

# def resample_image(input_path, output_path, xres=10, yres=10, resample_alg='bilinear'):
#     input_dataset = gdal.Open(input_path)
#     if input_dataset is None:
#         print("Error: Unable to open the input image.")
#         return
    
#     input_projection = input_dataset.GetProjection()
#     input_geotransform = input_dataset.GetGeoTransform()
    
#     if input_geotransform is None:
#         print("Error: Unable to retrieve geotransform information.")
#         return

#     # Calculate output dimensions based on new resolution
#     input_cols = input_dataset.RasterXSize
#     input_rows = input_dataset.RasterYSize
    
#     output_cols = round(input_cols * (input_geotransform[1] / xres))
#     output_rows = round(input_rows * (abs(input_geotransform[5]) / yres))

#     if output_cols <= 0 or output_rows <= 0:
#         print("Error: Invalid output size calculated.")
#         return

#     output_driver = gdal.GetDriverByName('GTiff')

#     # Create a virtual dataset for resampling
#     mem_drv = gdal.GetDriverByName('MEM')
#     mem_ds = mem_drv.Create('', output_cols, output_rows, 1, gdal.GDT_Float32)
#     mem_ds.SetGeoTransform((input_geotransform[0], xres, 0, input_geotransform[3], 0, -yres))
#     mem_ds.SetProjection(input_projection)

#     # Convert resample_alg to GDALResampleAlg type
#     resample_algorithm = getattr(gdal, 'GRA_NearestNeighbour')

#     # Perform the resampling
#     gdal.ReprojectImage(input_dataset, mem_ds, None, None, resample_algorithm)

#     # Create an output dataset and write the resampled data
#     output_ds = output_driver.CreateCopy(output_path, mem_ds, 0)
    
# def export_array_as_geotiff(array, output_path, geotransform):
#     # Get array shape and type
#     rows, cols = array.shape
#     dtype = array.dtype
    
#     # Create the GeoTIFF driver
#     driver = gdal.GetDriverByName("GTiff")

#     # Create a new GeoTIFF file
#     dataset = driver.Create(output_path, cols, rows, 1, gdal.GDT_Float32)

#     # Set the geotransform
#     dataset.SetGeoTransform(geotransform)

#     # Set the projection to EPSG:32629/32630
#     srs = osr.SpatialReference()
#     if '_30' in output_path:
#         srs.ImportFromEPSG(32630)
#     else:
#         srs.ImportFromEPSG(32629)
#     dataset.SetProjection(srs.ExportToWkt())

#     # Write the array data into the GeoTIFF
#     band = dataset.GetRasterBand(1)
#     band.WriteArray(array)

#     # Flush data to disk and close dataset
#     band.FlushCache()
#     dataset.FlushCache()
#     dataset = None

# list_tiles = [
#     # '29RMQ',
#     # '29RNQ',
#     # '29RPQ',
#     # '29RQQ',
#     # '29SMR',
#     # '29SMS',
#     # '29SNR',
#     # '29SNS',
#     # '29SNT',
#     # '29SPR',
#     # '29SPS',
#     # '29SPT',
#     # '29SQR',
#     # '29SQS',
#     # '29SQT',
#     '29SQU',
#     # '30STA',
#     # '30STB',
#     # '30STC',
#     # '30STD',
#     # '30SUA',
#     # '30SUB',
#     # '30SUC',
#     # '30SUD',
#     # '30SVB',
#     # '30SVC',
#     # '30SVD'
# ]

# bands = [
#     'B04',
#     'B08',
#     'B11',
#     'B12'
# ]

# directory = '202405b'

# path = f'D:/___DEEPFACES_SERVER/zar3i/NDTI_2023_2024/'

# images_B04 = os.listdir(path + bands[0])
# images_B08 = os.listdir(path + bands[1])
# images_B11 = os.listdir(path + bands[2])
# images_B12 = os.listdir(path + bands[3])

# for tile in list_tiles:
#     try:
#         print(tile)
#         list_ndvi_tile = []
#         list_ndti_tile = []
#         for i, image in enumerate(images_B04):
#             print(image)
#             if tile in image:
#                 try:
#                     B08_dataset, B08_array = readImage(os.path.join(path, 'B08', images_B08[i]))
#                     B04_dataset, B04_array = readImage(os.path.join(path, 'B04', images_B04[i]))
                    
#                     B11_dataset, B11_array = readImage(os.path.join(path, 'B11', images_B11[i]))
#                     B12_dataset, B12_array = readImage(os.path.join(path, 'B12', images_B12[i]))
                    
#                     NDVI = (calcNDVI(B08_array, B04_array)*10000).astype(np.int16)
#                     list_ndvi_tile.append(NDVI)
                    
#                     B11_path = path + 'B11/' + images_B11[i]
#                     output_path = f'D:/___DEEPFACES_SERVER/zar3i/NDTI_2023_2024/auxiliar/{images_B11[i][:-7]}resampled_10m.tif'
                   
#                     resample_image(B11_path, output_path)
#                     B11_dataset, B11_array = readImage(output_path)
                    
#                     B12_path = path + 'B12/' + images_B12[i]
#                     output_path = f'D:/___DEEPFACES_SERVER/zar3i/NDTI_2023_2024/auxiliar/{images_B12[i][:-7]}resampled_10m.tif'
                   
#                     resample_image(B12_path, output_path)
#                     B12_dataset, B12_array = readImage(output_path)
                    
#                     NDTI = (calcNDVI(B11_array, B12_array)*10000).astype(np.int16) 
#                     list_ndti_tile.append(NDTI)
                    
#                     del B08_array
#                     del B04_array
#                     del B11_array
#                     del NDMI
#                     del NDVI
#                 except:
#                     pass
        
#         img_NDVI = np.stack(list_ndvi_tile, axis = 0)
#         max_indices = np.argmax(img_NDVI, axis=0)
        
#         good_NDVI = qualityComposite(img_NDVI, max_indices)
#         mask = (good_NDVI/10000 >= -1) & (good_NDVI/10000 <= 1)
#         result_NDVI = np.where(mask, good_NDVI/10000, -9999)
#         export_array_as_geotiff(result_NDVI.astype(np.float32),  f'D:/___DEEPFACES_SERVER/zar3i/NDTI_2023_2024/NDVI/NDVI_{tile}.tif', B04_dataset.GetGeoTransform())
        
#         good_NDMI = qualityComposite(np.stack(list_ndti_tile, axis = 0), max_indices)
#         mask = (good_NDMI/10000 >= -1) & (good_NDMI/10000 <= 1)
#         result_NDMI = np.where(mask, good_NDMI/10000, -9999)    
#         export_array_as_geotiff(result_NDMI.astype(np.float32),  f'D:/___DEEPFACES_SERVER/zar3i/NDTI_2023_2024/NDTI/NDTI_{tile}.tif', B04_dataset.GetGeoTransform())
#     except:
#         pass