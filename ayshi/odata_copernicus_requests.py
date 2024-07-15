# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 12:29:45 2023

@author: joaos
"""

import requests
import concurrent.futures
import time
from retrying import retry

################ EDITAR ##############
month = '06'
directory_update = f'2024{month}d'
######################################

def constructAttQuery(attType, att, operator, value):
    """
    attType in ['StringAttribute', 'DoubleAttribute', 'IntegerAttribute', 'DateTimeOffsetAttribute']
    
    att...
    
    operator in ['eq', 'le', 'lt', 'ge', 'gt']
    
    value...
    """
    if attType == 'StringAttribute':
        return f"Attributes/OData.CSC.{attType}/any(att:att/Name eq '{att}' and att/OData.CSC.ValueTypeAttribute/Value {operator} '{value}')"
    else:
        return f"Attributes/OData.CSC.{attType}/any(att:att/Name eq '{att}' and att/OData.CSC.ValueTypeAttribute/Value {operator} {value})"

@retry(wait_fixed=2000, stop_max_attempt_number=5)  # Wait 2 seconds between retries, try at most 5 times
def get_with_retry(url, headers=None, params=None):
    response = requests.get(url, headers=headers, params=params, stream = True)
    response.raise_for_status()  # Raise an HTTPError for bad responses
    return response

def download_band(url_download, destination):
    with get_with_retry(url_download, headers=headers_download) as response:
        print(url_download[-40:-10])
        print(response)
        with open(destination, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

tiles = [
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

month_days = {
    '01':'31',
    '02':'28',
    '03':'31',
    '04':'30',
    '05':'31',
    '06':'30',
    '07':'31',
    '08':'31',
    '09':'30',
    '10':'31',
    '11':'30',
    '12':'31'
}

bands_10m = [
    'B04',
    'B08'
]

bands_20m = [
    'B11'
]
#%% Token

url_token = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
}

data = {
    "grant_type": "password",
    "username": "joao.sa@greenworld.pt",
    "password": "4lphaJk99!#%",
    "client_id": "cdse-public"
}

def getToken(url_token, headers, data):
    response_token = requests.post(url_token, headers=headers, data=data)
    return response_token.json()['access_token']

#%% Query

url_query = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter="

# startDate = f'2024-{month}-01'
# #endDate = f'2023-{month}-{month_days[month]}'
# endDate = f'2024-{month}-19' # week updates

################# EDITAR ######################
startDate = '2024-06-21'
endDate = '2024-06-30'
############################################

productIDs = []
#tiles = ['29RNQ', '29RMQ', '30SVB', '30SVC', '30SVD']
for tile in tiles:    
    try:
        filter_query = f"(startswith(Name,'S2') and contains(Name, '{tile}')) and {constructAttQuery('StringAttribute', 'productType', 'eq', 'S2MSI2A')} and {constructAttQuery('DoubleAttribute', 'cloudCover', 'lt', 70)} and ContentDate/Start gt {startDate}T00:00:00.000Z and ContentDate/End lt {endDate}T23:59:59.999Z"
        
        #filter_query = "Name eq 'S1A_IW_GRDH_1SDV_20141031T161924_20141031T161949_003076_003856_634E.SAFE'"
        url_query_request = url_query + filter_query
        
        response_query = requests.get(url_query_request)
        print(tile)
        print(response_query.status_code)
        print(len(response_query.json()['value']))
        for value in response_query.json()['value']:
            productIDs.append([value['Id'], value['Name']])
    except:
        print(f'ERROR for tile {tile}')

#%% Downloads
# for product in productIDs:
#     access_token = getToken(url_token, headers, data)
    
#     headers = {"Authorization": f"Bearer {access_token}"}
    
#     url_node_granule_child = f"https://zipper.dataspace.copernicus.eu/odata/v1/Products({product[0]})/Nodes({product[1]})/Nodes(GRANULE)/Nodes"
    
#     response_query = requests.get(url_node_granule_child)
#     url_imgs = response_query.json()['result'][0]['Nodes']['uri'] + "(IMG_DATA)/Nodes"
    
#     url_imgs_r10 = url_imgs + "(R10m)/Nodes"
#     url_imgs_r20 = url_imgs + "(R20m)/Nodes"
    
#     response_imgs10m = requests.get(url_imgs_r10)
#     url_imgs10m = response_imgs10m.json()['result']
#     for band in bands_10m:
#         for obj in response_imgs10m.json()['result']:
#             if f"_{band}_" in obj['Name']:
#                 url_download = obj['Nodes']['uri'][:-5] + "$value"
#                 session = requests.Session()
#                 session.headers.update(headers)
#                 response = session.get(url_download, headers=headers, stream=True)
                
#                 with open(f"C:/Users/joaos/OneDrive/Ambiente de Trabalho/DF/zar3i/1_bands_teste/{band}/{obj['Name']}", "wb") as file:
#                     for chunk in response.iter_content(chunk_size=8192):
#                         if chunk:
#                             file.write(chunk)
    
#     response_imgs20m = requests.get(url_imgs_r20)
#     url_imgs20m = response_imgs20m.json()['result']
#     for band in bands_20m:
#         for obj in response_imgs20m.json()['result']:
#             if f"_{band}_" in obj['Name']:
#                 url_download = obj['Nodes']['uri'][:-5] + "$value"
#                 session = requests.Session()
#                 session.headers.update(headers)
#                 response = session.get(url_download, headers=headers, stream=True)
                
#                 with open(f"C:/Users/joaos/OneDrive/Ambiente de Trabalho/DF/zar3i/1_bands_teste/{band}/{obj['Name']}", "wb") as file:
#                     for chunk in response.iter_content(chunk_size=8192):
#                         if chunk:
#                             file.write(chunk)

#%% Download (GPT)

access_token = getToken(url_token, headers, data)
t_b = time.localtime()[3] * 60 + time.localtime()[4] + time.localtime()[5]/60
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    for product in productIDs:
        try:
            t_s = time.localtime()[3] * 60 + time.localtime()[4] + time.localtime()[5]/60
            print(t_s - t_b)
            if t_s - t_b >= 8:
                print('Novo pedido de token!')
                access_token = getToken(url_token, headers, data)
                t_b = t_s
                
            headers_download = {"Authorization": f"Bearer {access_token}"}
            print(product)
            url_node_granule_child = f"https://zipper.dataspace.copernicus.eu/odata/v1/Products({product[0]})/Nodes({product[1]})/Nodes(GRANULE)/Nodes"
            response_query = requests.get(url_node_granule_child)
            url_imgs = response_query.json()['result'][0]['Nodes']['uri'] + "(IMG_DATA)/Nodes"

            url_imgs_r10 = url_imgs + "(R10m)/Nodes"
            url_imgs_r20 = url_imgs + "(R20m)/Nodes"

            response_imgs10m = get_with_retry(url_imgs_r10)
            url_imgs10m = response_imgs10m.json()['result']

            for band in bands_10m:
                for obj in response_imgs10m.json()['result']:
                    if f"_{band}_" in obj['Name']:
                        url_download = obj['Nodes']['uri'][:-5] + "$value"
                        destination = f"D:/___DEEPFACES_SERVER/zar3i_site_updates/{directory_update}/1_bands/{band}/{obj['Name']}"
                        futures.append(executor.submit(download_band, url_download, destination)) 
                        time.sleep(5)
                        
            response_imgs20m = get_with_retry(url_imgs_r20)
            url_imgs20m = response_imgs20m.json()['result']
    
            for band in bands_20m:
                for obj in response_imgs20m.json()['result']:
                    if f"_{band}_" in obj['Name']:
                        url_download = obj['Nodes']['uri'][:-5] + "$value"
                        destination = f"D:/___DEEPFACES_SERVER/zar3i_site_updates/{directory_update}/1_bands/{band}/{obj['Name']}"
                        futures.append(executor.submit(download_band, url_download, destination))
                        time.sleep(5)
                        
            time.sleep(5)
            del response_query
            del response_imgs10m
        except:
            print(f'ERROR!!! retry {product}')

# Wait for all downloads to complete
concurrent.futures.wait(futures)