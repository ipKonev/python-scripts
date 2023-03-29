from pprint import pprint
import json
import requests
from requests.auth import HTTPBasicAuth
from requests.packages import urllib3
import os


#Скрипт запрашивает группы объектов на FTD


#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_gid(gname,accesstoken,refreshtoken,GLOBAL_UUID,DOMAIN_UUID):

    host_api_uri=f'/api/fmc_config/v1/domain/{DOMAIN_UUID}/object/networkgroups'
    host_url=f'https://{os.environ["FMCADDR"]}{host_api_uri}?offset=0&limit=1000'
    headers={ 'Content-Type': 'application/json', 'x-auth-access-token': accesstoken }

    response=requests.request("GET", host_url, headers=headers, verify=False)

    group=response.json()['items']
    for each in group:
        if each['name'] == gname:
            value=each['id']
    return value


if __name__ == '__main__':
   print(get_gid('VPN-KONEV-4')) 
