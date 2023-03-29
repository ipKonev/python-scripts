import os
import json
import requests
from requests.auth import HTTPBasicAuth
from requests.packages import urllib3
from pprint import pprint
import socket

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def create_ace(hosts):
    ace_list=[]
    for host in hosts:
        addr,mask,proto,ports=host
        ports=str(ports).split(',')
        for port in ports:
            if '-' in port:
                port1,port2=port.split('-')
                ace=f'permit {proto} any {addr} {mask} range {port1} {port2}'
            else:
                ace=f'permit {proto} any {addr} {mask} eq {port}'
            ace_list.append(ace)
    return '\n'.join(ace_list)

def create_acl(ace,pName):
    dict1={
  "DownloadableAcl": {
    "name": f"ACL-{pName}",
    "description": "description",
    "dacl": ace,
    "daclType": "IPV4"}}
#Приведенный header корректно работает с POST
    header={'Accept': 'application/json','Content-Type': 'application/json', 'charset': 'utf-8', 'username': os.environ['ERSADMIN'], 'password': os.environ['ERSPASS']}
    headers=header
    user=header['username']
    password=header['password']
    url=f'https://{os.environ["FMCADDR"]}/ers/config/downloadableacl'
    response=requests.post(url,auth=HTTPBasicAuth(user,password),headers=headers,data=json.dumps(dict1), verify=False)
    data1=response.status_code
    return data1

if __name__=='__main__':
    pName='VPN-Konev'
    ace=create_ace(dnslist,hlist,plist,pName)
    pprint(create_acl(ace,pName))
