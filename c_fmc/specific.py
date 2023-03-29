from pprint import pprint
import json
import requests
import time
from requests.auth import HTTPBasicAuth
from requests.packages import urllib3
import os

from create_token import rcv_token

#Получаем текущие значения NetworkObject


def get_object_info(gid,accesstoken,refreshtoken,GLOBAL_UUID,DOMAIN_UUID):

    host_api_uri=f'/api/fmc_config/v1/domain/{DOMAIN_UUID}/object/networkgroups/'
    host_url=f'https://{os.environ["FMCADDR"]}{host_api_uri}{gid}'
    headers={ 'Content-Type': 'application/json', 'x-auth-access-token': accesstoken }

    response=requests.request("GET", host_url, headers=headers, verify=False)

    obj_dict={"id": response.json()['id'],
    "name": response.json()['name'],
    "type": response.json()['type'],
    "literals": response.json()['literals']}
    return obj_dict


