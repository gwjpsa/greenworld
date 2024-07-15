import os

def TIF2colorPNG(listImgs, colorTable, pathOut):
    
    redNDVI = []
    greenNDVI = []
    blueNDVI = []

    for k in colorTable.keys():
        redNDVI+=[colorTable[k]['minValue'], colorTable[k]['maxValue'], colorTable[k]['R']]
        greenNDVI+=[colorTable[k]['minValue'], colorTable[k]['maxValue'], colorTable[k]['G']]
        blueNDVI+=[colorTable[k]['minValue'], colorTable[k]['maxValue'], colorTable[k]['B']]

    for img in listImgs:

        global reclassifyR 
        reclassifyR = processing.run("native:reclassifybytable", {
            'INPUT_RASTER':img.source(),
            'RASTER_BAND':1,
            'TABLE':redNDVI,
            'NO_DATA':-9999,
            'RANGE_BOUNDARIES':1,
            'NODATA_FOR_MISSING':False,
            'DATA_TYPE':1,
            'OUTPUT':'TEMPORARY_OUTPUT'
        })['OUTPUT']
        raster_layer_reclassifyR = QgsRasterLayer(reclassifyR, 'ndviRed')
        #QgsProject.instance().addMapLayer(raster_layer_reclassifyR, True)
        
        global reclassifyG
        reclassifyG = processing.run("native:reclassifybytable", {
            'INPUT_RASTER':img.source(),
            'RASTER_BAND':1,
            'TABLE':greenNDVI,
            'NO_DATA':-9999,
            'RANGE_BOUNDARIES':1,
            'NODATA_FOR_MISSING':False,
            'DATA_TYPE':1,
            'OUTPUT':'TEMPORARY_OUTPUT'
        })['OUTPUT']
        raster_layer_reclassifyG = QgsRasterLayer(reclassifyG, 'ndviGreen')
        #QgsProject.instance().addMapLayer(raster_layer_reclassifyG, True)
        
        global reclassifyB 
        reclassifyB = processing.run("native:reclassifybytable", {
            'INPUT_RASTER':img.source(),
            'RASTER_BAND':1,
            'TABLE':blueNDVI,
            'NO_DATA':-9999,
            'RANGE_BOUNDARIES':1,
            'NODATA_FOR_MISSING':False,
            'DATA_TYPE':1,
            'OUTPUT':'TEMPORARY_OUTPUT'
        })['OUTPUT']
        raster_layer_reclassifyB = QgsRasterLayer(reclassifyB, 'ndviBlue')
        #QgsProject.instance().addMapLayer(raster_layer_reclassifyB, True

        merged = processing.run("gdal:merge", {
            'INPUT':[reclassifyR, reclassifyG, reclassifyB],
            'PCT':False,
            'SEPARATE':True,
            'NODATA_INPUT':-9999,
            'NODATA_OUTPUT':-9999,
            'OPTIONS':'',
            'EXTRA':'',
            'DATA_TYPE':0,
            'OUTPUT':'TEMPORARY_OUTPUT'
        })['OUTPUT']
        raster_layer_merge = QgsRasterLayer(merged, 'merged')
        #QgsProject.instance().addMapLayer(raster_layer_merge, True)
        
        toPNG = processing.run("gdal:translate", {
            'INPUT':merged,
            'TARGET_CRS':None,
            'NODATA':None,
            'COPY_SUBDATASETS':False,
            'OPTIONS':'',
            'EXTRA':'',
            'DATA_TYPE':1,
            'OUTPUT':pathOut+img.name()+'.png'
        })['OUTPUT']
        raster_layer_toPNG = QgsRasterLayer(toPNG, 'final')
        #QgsProject.instance().addMapLayer(raster_layer_toPNG, True)
        #break

def getListImgs(path):

    listDirectory = os.listdir(path)
    listImgs = []

    for file in listDirectory:
        if '_9999' in file and file[-4:] == '.tif':
            listNDMI_int16.append(file)
    
    listImgs.sort()
    return(listImgs)

pathNDVI = 'D:/___DEEPFACES_SERVER/zar3i_site_updates/'+dir_update+'/3_communesV/NDVI/'
pathNDMI = 'D:/___DEEPFACES_SERVER/zar3i_site_updates/'+dir_update+'/3_communesV/NDMI/'

listDirNDVI = os.listdir(pathNDVI)
listDirNDMI = os.listdir(pathNDMI)

listDirNDVI.sort()
listDirNDMI.sort()

listImgsNDVI = []
listImgsNDMI = []

for file in listDirNDVI:
    if file[-4:] == '.tif' in file:
        listImgsNDVI.append(file)

for file in listDirNDMI:
    if file[-4:] == '.tif' in file:
        listImgsNDMI.append(file)

listNDVI_int16 = []
listNDMI_int16 = []
listCropRisk_int16 = []
listAvgYield_int16 = []

pathOutTemps= 'D:/___DEEPFACES_SERVER/zar3i_site_updates/'+dir_update+'/4_communesPNG/_tempAux/'

for i in range(len(listImgsNDMI)):
    NDMIint16 = processing.run("gdal:rastercalculator", {
        'INPUT_A':pathNDMI + listImgsNDMI[i],
        'BAND_A':1,
        'INPUT_B':None,
        'BAND_B':None,
        'INPUT_C':None,
        'BAND_C':None,
        'INPUT_D':None,
        'BAND_D':None,
        'INPUT_E':None,
        'BAND_E':None,
        'INPUT_F':None,
        'BAND_F':None,
        'FORMULA':'A*100',
        'NO_DATA':-9999,
        'PROJWIN':None,
        'RTYPE':1,
        'OPTIONS':'',
        'EXTRA':'',
        'OUTPUT':pathOutTemps+listImgsNDMI[i][:-4]+'_ndmi16.tif'
    })['OUTPUT']
    raster_layer_NDMIint16 = QgsRasterLayer(NDMIint16,listImgsNDMI[i][:-4])
    #QgsProject.instance().addMapLayer(raster_layer_NDMIint16)
    listNDMI_int16.append(raster_layer_NDMIint16)
    
    NDVIint16 = processing.run("gdal:rastercalculator", {
        'INPUT_A':pathNDVI + listImgsNDVI[i],
        'BAND_A':1,
        'INPUT_B':None,
        'BAND_B':None,
        'INPUT_C':None,
        'BAND_C':None,
        'INPUT_D':None,
        'BAND_D':None,
        'INPUT_E':None,
        'BAND_E':None,
        'INPUT_F':None,
        'BAND_F':None,
        'FORMULA':'A*100',
        'NO_DATA':-9999,
        'PROJWIN':None,
        'RTYPE':1,
        'OPTIONS':'',
        'EXTRA':'',
        'OUTPUT':pathOutTemps+listImgsNDMI[i][:-4]+'_ndvi16.tif'
    })['OUTPUT']
    raster_layer_NDVIint16 = QgsRasterLayer(NDVIint16,listImgsNDVI[i][:-4])
    #QgsProject.instance().addMapLayer(raster_layer_NDVIint16)
    listNDVI_int16.append(raster_layer_NDVIint16)

    NDMI_clip = processing.run("gdal:cliprasterbyextent", {
        'INPUT':pathNDMI + listImgsNDMI[i],
        'PROJWIN':raster_layer_NDVIint16.extent(),
        'OVERCRS':False,
        'NODATA':-9999,
        'OPTIONS':'',
        'DATA_TYPE':0,
        'EXTRA':'',
        'OUTPUT':pathOutTemps+listImgsNDMI[i][:-4]+'_clipTemp.tif'
    })['OUTPUT']
    raster_layer_NDMI_clip = QgsRasterLayer(NDMI_clip, listImgsNDMI[i][:-4])
    #QgsProject.instance().addMapLayer(raster_layer_NDMI_clip)

    cropRisk = processing.run("gdal:rastercalculator", {
        'INPUT_A':pathNDVI + listImgsNDVI[i],
        'BAND_A':1,
        'INPUT_B':NDMI_clip,
        'BAND_B':1,
        'INPUT_C':None,
        'BAND_C':None,
        'INPUT_D':None,
        'BAND_D':None,
        'INPUT_E':None,
        'BAND_E':None,
        'INPUT_F':None,
        'BAND_F':None,
        'FORMULA':'(((1-(A))+(2-(1+(B)))/2)/2)*100',
        'NO_DATA':-9999,
        'PROJWIN':None,
        'RTYPE':1,
        'OPTIONS':'',
        'EXTRA':'',
        'OUTPUT':pathOutTemps+listImgsNDMI[i][:-4]+'_croprisk.tif'
    })['OUTPUT']
    raster_layer_CropRisk = QgsRasterLayer(cropRisk, listImgsNDMI[i][:-4])
    #QgsProject.instance().addMapLayer(raster_layer_CropRisk)
    listCropRisk_int16.append(raster_layer_CropRisk)

    avgYield = processing.run("gdal:rastercalculator", {
        'INPUT_A':cropRisk,
        'BAND_A':1,
        'INPUT_B':None,
        'BAND_B':None,
        'INPUT_C':None,
        'BAND_C':None,
        'INPUT_D':None,
        'BAND_D':None,
        'INPUT_E':None,
        'BAND_E':None,
        'INPUT_F':None,
        'BAND_F':None,
        'FORMULA':'(5 - 5 * A/100)*100',
        'NO_DATA':-9999,
        'PROJWIN':None,
        'RTYPE':1,
        'OPTIONS':'',
        'EXTRA':'',
        'OUTPUT':pathOutTemps+listImgsNDMI[i][:-4]+'_avgYield.tif'
    })['OUTPUT']
    raster_layer_AvgYield = QgsRasterLayer(avgYield, listImgsNDMI[i][:-4])
    listAvgYield_int16.append(raster_layer_AvgYield)

## NDVI
pathOutNDVI = 'D:/___DEEPFACES_SERVER/zar3i_site_updates/'+dir_update+'/4_communesPNG/NDVI/id_'

colorTableNDVI = {
    0:{'minValue':-100, 'maxValue': 10, 'R':165, 'G':  1, 'B': 38},
    1:{'minValue':  10, 'maxValue': 20, 'R':215, 'G': 48, 'B': 39},
    2:{'minValue':  20, 'maxValue': 30, 'R':253, 'G':174, 'B': 97},
    3:{'minValue':  30, 'maxValue': 40, 'R':254, 'G':224, 'B':139},
    4:{'minValue':  40, 'maxValue': 50, 'R':255, 'G':255, 'B':191},
    5:{'minValue':  50, 'maxValue': 60, 'R':217, 'G':239, 'B':139},
    6:{'minValue':  60, 'maxValue': 70, 'R':166, 'G':217, 'B':106},
    7:{'minValue':  70, 'maxValue': 80, 'R':102, 'G':189, 'B': 99},
    8:{'minValue':  80, 'maxValue': 90, 'R': 26, 'G':152, 'B': 80},
    9:{'minValue':  90, 'maxValue':100, 'R': 26, 'G':150, 'B': 65}
}

TIF2colorPNG(listNDVI_int16, colorTableNDVI, pathOutNDVI)
del listNDVI_int16

## NDMI
pathOutNDMI = 'D:/___DEEPFACES_SERVER/zar3i_site_updates/'+dir_update+'/4_communesPNG/NDMI/id_'

colorTableNDMI = {
    0:{'minValue':-100, 'maxValue':-80, 'R':171, 'G':  1, 'B':  1},
    1:{'minValue': -80, 'maxValue':-60, 'R':255, 'G':  1, 'B':  1},
    2:{'minValue': -60, 'maxValue':-40, 'R':255, 'G':127, 'B':  1},
    3:{'minValue': -40, 'maxValue':-20, 'R':255, 'G':189, 'B':127},
    4:{'minValue': -20, 'maxValue':  0, 'R':255, 'G':255, 'B':127},
    5:{'minValue':   1, 'maxValue': 20, 'R':195, 'G':255, 'B': 76},
    6:{'minValue':  20, 'maxValue': 40, 'R':127, 'G':255, 'B':191},
    7:{'minValue':  40, 'maxValue': 60, 'R':127, 'G':255, 'B':255},
    8:{'minValue':  60, 'maxValue': 80, 'R':113, 'G':234, 'B':248},
    9:{'minValue':  80, 'maxValue':100, 'R':  1, 'G': 63, 'B':191}
}

TIF2colorPNG(listNDMI_int16, colorTableNDMI, pathOutNDMI)
del listNDMI_int16

## cropRisk
pathOutCropRisk = 'D:/___DEEPFACES_SERVER/zar3i_site_updates/'+dir_update+'/4_communesPNG/Crop_Risk/id_'

colorTableCropRisk = {
    0:{'minValue': 0, 'maxValue': 20, 'R':  1, 'G':127, 'B': 63},
    1:{'minValue':20, 'maxValue': 40, 'R':166, 'G':217, 'B':106},
    2:{'minValue':40, 'maxValue': 60, 'R':255, 'G':255, 'B':192},
    3:{'minValue':60, 'maxValue': 80, 'R':255, 'G':127, 'B': 63},
    4:{'minValue':80, 'maxValue':100, 'R':171, 'G':  1, 'B':  1}
}

#TIF2colorPNG(listCropRisk_int16, colorTableCropRisk, pathOutCropRisk)
del listCropRisk_int16

## Avg yield
pathOutAvgYield = 'D:/___DEEPFACES_SERVER/zar3i_site_updates/'+dir_update+'/4_communesPNG/Harvest_Forecast/id_'
print('ola')
colorTableAverageYield = {
    0:{'minValue':  0, 'maxValue': 50, 'R':192, 'G':  1, 'B':  1},
    1:{'minValue': 50, 'maxValue':100, 'R':200, 'G': 69, 'B':  1},
    2:{'minValue':100, 'maxValue':150, 'R':248, 'G':138, 'B':  1},
    3:{'minValue':150, 'maxValue':200, 'R':255, 'G':188, 'B': 42},
    4:{'minValue':200, 'maxValue':250, 'R':255, 'G':233, 'B': 99},
    5:{'minValue':250, 'maxValue':300, 'R':233, 'G':255, 'B':133},
    6:{'minValue':300, 'maxValue':350, 'R':188, 'G':255, 'B':146},
    7:{'minValue':350, 'maxValue':400, 'R':138, 'G':239, 'B':158},
    8:{'minValue':400, 'maxValue':450, 'R': 69, 'G':177, 'B':172},
    9:{'minValue':450, 'maxValue':500, 'R':  1, 'G':115, 'B':186}
}

TIF2colorPNG(listAvgYield_int16, colorTableAverageYield, pathOutAvgYield)
del listAvgYield_int16