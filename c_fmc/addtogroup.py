from pprint import pprint
import json
import requests
import time
from requests.auth import HTTPBasicAuth
from requests.packages import urllib3
import os

from specific import get_object_info 
from create_token import rcv_token
from getgrp import get_gid

#Скрипт создает группу объектов на FTD



def update_statements(gname,literals):
    accesstoken,refreshtoken,GLOBAL_UUID,DOMAIN_UUID=rcv_token()
    gid=get_gid(gname,accesstoken,refreshtoken,GLOBAL_UUID,DOMAIN_UUID)
    statements=get_object_info(gid,accesstoken,refreshtoken,GLOBAL_UUID,DOMAIN_UUID)
    statements['literals'].extend(literals)
    pprint(statements['literals'])
#Обязательная команда, для корректной отправки
    host_payload=json.dumps(statements)

    host_api_uri=f'/api/fmc_config/v1/domain/{DOMAIN_UUID}/object/networkgroups/'
    host_url=f'https://{os.environ["FMCADDR"]}{host_api_uri}{gid}'
    headers={ 'Content-Type': 'application/json', 'x-auth-access-token': accesstoken }

    response=requests.request("PUT", host_url, headers=headers, data=host_payload, verify=False)

    if response.status_code == 200 or response.status_code == 201 or response.status.code == 202:
        print('Host object successfully pushed')
    else:
        print("Operation has been failed")

if __name__ == '__main__':
    literals=[{"type": "Network","value": "192.52.55.0/24"},{"type": "Host","value": "201.25.32.44"}]
    update_statements('VPN-KONEV-4',literals)
