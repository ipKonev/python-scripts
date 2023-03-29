import os
import json
import requests
from requests.auth import HTTPBasicAuth
from requests.packages import urllib3
from pprint import pprint
import socket

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def create_auth(pName):
    dict1={
  "AuthorizationProfile": {
    "name": pName,
    "description": "description",
    "accessType": "ACCESS_ACCEPT",
    "daclName": f'ACL-{pName}'}}
#Приведенный header корректно работает с POST
    header={'Accept': 'application/json','Content-Type': 'application/json', 'charset': 'utf-8', 'username': os.environ['ERSADMIN'], 'password': os.environ['ERSPASS']}
    headers=header
    user=header['username']
    password=header['password']
    url='https://{os.environ["FMCADDR"]}/ers/config/authorizationprofile'
    response=requests.post(url,auth=HTTPBasicAuth(user,password),headers=headers,data=json.dumps(dict1), verify=False)
    data1=response.status_code
    return data1

if __name__=='__main__':
    #ace=create_ace(hlist,plist)
    pprint(create_auth('VPN-Konev'))