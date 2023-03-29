import json
import requests
import time
from requests.auth import HTTPBasicAuth
from requests.packages import urllib3
import os

#Скрипт создает группу объектов на FTD

hosts={
    "name": "VPN-KONEV-5",
    "literals": [
        {
            "type": "Network",
            "value": "1.2.3.0/24"
        },
        {
            "type": "Host",
            "value": "1.2.3.4"
        }
    ],
    "overridable": False,
    "type": "NetworkGroup"
}
#Обязательная команда, для корректной отправки
host_payload=json.dumps(hosts)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

api_uri='/api/fmc_platform/v1/auth/generatetoken'
url=f'https://{os.environ["FMCADDR"]}{api_uri}'

response=requests.request("POST", url, verify=False, auth=HTTPBasicAuth(os.environ['FMCUSER'], os.environ['FMCPASS']))

accesstoken=response.headers['X-auth-access-token']
refreshtoken=response.headers['X-auth-refresh-token']
DOMAIN_UUID=(json.loads(response.headers['DOMAINS'])[1])['uuid']
print(DOMAIN_UUID)

host_api_uri=f'/api/fmc_config/v1/domain/{DOMAIN_UUID}/object/networkgroups'
host_url=f'https://{os.environ["FMCADDR"]}{host_api_uri}'
headers={ 'Content-Type': 'application/json', 'x-auth-access-token': accesstoken }

print(host_payload)
if hosts != []:
    response=requests.request("POST", host_url, headers=headers, data=host_payload, verify=False)

if response.status_code == 200 or response.status_code == 201 or response.status.code == 202:
    print('Host object successfully pushed')
else:
    print("Operation has been failed")
