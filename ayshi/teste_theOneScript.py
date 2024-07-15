tenants = ['zar3i','icarda']  
dir_update = '202406d'
dateToday_format = '30/06/2024'

exec(open('D:/___DEEPFACES_SERVER/zar3i/scripts/updates/0_greenWorldPyQgis.py').read())
#exec(open('D:/___DEEPFACES_SERVER/zar3i/scripts/updates/1_mergeTiles2324.py').read())
#print('Merge Tiles - finalizado')

#for i in range(17):
#    print(i+1)
#    job_it = i + 1
#    exec(open('D:/___DEEPFACES_SERVER/zar3i/scripts/updates/2_iterateOverCommunes.py').read())
#    print(f'iterate over communes {i} - finalizado')
#
#exec(open('D:/___DEEPFACES_SERVER/zar3i/scripts/updates/2_1_merge_zstats.py').read())
#print('zstats - finalizado')
#
#exec(open('D:/___DEEPFACES_SERVER/zar3i/scripts/updates/3_0_zar3i_auxiliaryScript_listMissingFieldValuesByCommune_id.py').read())
#exec(open('D:/___DEEPFACES_SERVER/zar3i/scripts/updates/3_1_zar3i_NDVI_NDMI_insertToDB_final.py').read())
#exec(open('D:/___DEEPFACES_SERVER/zar3i/scripts/updates/3_2_zar3i_icarda_NDVI_NDMI_insertToDB_fields_final.py').read())
#print('updates BD - finalizado')

#exec(open('D:/___DEEPFACES_SERVER/zar3i/scripts/updates/4_TIF1b_to_PNG4b.py').read())
#print('TIF 1band to PNG 4 bands - finalizado')

#exec(open('D:/___DEEPFACES_SERVER/zar3i/scripts/updates/5_v2_interpolation_meteo.py').read())
#print('Interpolation Meteo - finalizado')
#exec(open('D:/___DEEPFACES_SERVER/zar3i/scripts/updates/5_1_zar3i_interpolation_fieldmeteo.py').read())

exec(open('D:/___DEEPFACES_SERVER/zar3i/scripts/updates/6_NDVI_fieldsByCommune.py').read())
