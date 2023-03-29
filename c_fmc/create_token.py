from pprint import pprint
import json
import requests
import time
from requests.auth import HTTPBasicAuth
from requests.packages import urllib3
import os

#Функция создает авторизационный токен, и возвращает информацию о доступных доменах
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def rcv_token():

    api_uri='/api/fmc_platform/v1/auth/generatetoken'
    url=f'https://{os.environ["FMCADDR"]}{api_uri}'
    response=requests.request("POST", url, verify=False, auth=HTTPBasicAuth(os.environ['FMCUSER'], os.environ['FMCPASS']))
    accesstoken=response.headers['X-auth-access-token']
    refreshtoken=response.headers['X-auth-refresh-token']
    GLOBAL_UUID=(json.loads(response.headers['DOMAINS'])[0])['uuid']
    DOMAIN_UUID=(json.loads(response.headers['DOMAINS'])[1])['uuid']

    return accesstoken,refreshtoken,GLOBAL_UUID,DOMAIN_UUID


if __name__ == '__main__':
    print(rcv_token())
