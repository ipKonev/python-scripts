import json
import requests
import time
from requests.auth import HTTPBasicAuth
from requests.packages import urllib3
import os

hosts=[{
        "name": "Konev-7",
        "description": "Konev-7",
        "type": "Konev",
        "value": "192.198.255.7"
    },
    {
        "name": "Konev-8",
        "description": "Konev-8",
        "type": "Konev",
        "value": "192.198.255.8"
    },
    {
        "name": "Konev-9",
        "description": "Konev-9",
        "type": "Konev",
        "value": "192.198.255.9"
    }
]

host_payload=json.dumps(hosts)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

api_uri='/api/fmc_platform/v1/auth/generatetoken'
url=f'https://{os.environ["FMCADDR"]}{api_uri}'

response=requests.request("POST", url, verify=False, auth=HTTPBasicAuth(os.environ['FMCUSER'], os.environ['FMCPASS']))

accesstoken=response.headers['X-auth-access-token']
refreshtoken=response.headers['X-auth-refresh-token']
DOMAIN_UUID=(json.loads(response.headers['DOMAINS'])[1])['uuid']

host_api_uri=f'/api/fmc_config/v1/domain/{DOMAIN_UUID}/object/hosts?bulk=true'
host_url=f'https://{os.environ["FMCADDR"]}{host_api_uri}'
headers={ 'Content-Type': 'application/json', 'x-auth-access-token': accesstoken }

print(host_payload)
if hosts != []:
    response=requests.request("POST", host_url, headers=headers, data=host_payload, verify=False)

if response.status_code == 201 or response.status.code == 202:
    print('Host object successfully pushed')
else:
    print("Operation has been failed")
