import ipaddress
import time
import datetime
import os
import json
import requests
from requests.auth import HTTPBasicAuth
from requests.packages import urllib3
from pprint import pprint
import socket

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def getalldacl():
    headers={'Accept': 'application/json'}
    summary={}
    i=1
    while True:
        url=f"{os.environ['ERSPATH']}/downloadableacl?page={i}"
        response=requests.request('GET',url,auth=HTTPBasicAuth(os.environ['ERSADMIN'],os.environ['ERSPASS']),headers=headers, verify=False)
        data=response.json()
        try:
            if data['SearchResult']['total'] != 0:
                dacl_list=data['SearchResult']['resources']
                for each in dacl_list:
                    summary[each['name']]=each['id']
                i+=1
            else:
                break
        except KeyError:
            break
    return summary

def get_by_id(dacl_id):
    header={'Accept': 'application/json','Content-Type': 'application/json', 'charset': 'utf-8', 'username': os.environ['ERSADMIN'], 'password': os.environ['ERSPASS']}
    headers=header
    user=header['username']
    password=header['password']
    url=f"{os.environ['ERSPATH']}/downloadableacl/{dacl_id}"
    response=requests.get(url,auth=HTTPBasicAuth(user,password),headers=headers, verify=False)
    #data1=response.status_code
    #return type(response.json()['DownloadableAcl']['dacl'])
    return response.json()

def get_content(dacl_dict):
    content_list=dacl_dict['DownloadableAcl']['dacl'].split('\n')
    return content_list

def validate_addr(addr):
    try:
        ipaddress.ip_address(addr)
        return True
    except ValueError:
        return False

def validate_network(addr):
    try:
        ipaddress.ip_network(addr)
        return True
    except ValueError:
        return False

def add_content(content_list,additional_content,ticket=None,dacl_name=''):
    content_list.append(f'Remark ----- {ticket} -----')
    for addr in additional_content:
        if validate_addr(addr) == True:
            ace=f'permit ip any host {addr}' 
        elif validate_network(addr) == True:
            network=ipaddress.ip_network(addr).network_address
            netmask=ipaddress.ip_network(addr).netmask
            ace=f'permit ip any {network} {netmask}'
        content_list.append(ace)
    return content_list


def uniq_content_verif(content_list):
    uniq_content_list = []
    for statement in content_list:
        if statement in uniq_content_list: continue
        else: uniq_content_list.append(statement)
    return uniq_content_list

def put_content(dacl_name,dacl_id,content):
        dacl={
          "DownloadableAcl" : {
            "id" : f"{dacl_id}",
            "name": f"{dacl_name}",
            "dacl" : "\n".join(content),
            "description" : f"LAST MODIFIED: {datetime.date.today()}",
            "daclType" : "IPV4"}}
        header={'Accept': 'application/json','Content-Type': 'application/json', 'charset': 'utf-8', 'username': os.environ['ERSADMIN'], 'password': os.environ['ERSPASS']}
        headers=header
        user=header['username']
        password=header['password']
        url=f"{os.environ['ERSPATH']}/downloadableacl/{dacl_id}"
        response=requests.put(url,auth=HTTPBasicAuth(user,password),headers=headers,data=json.dumps(dacl), verify=False)
        data1=response.status_code
        print(data1)
        #pprint(response.json())



if __name__=="__main__":
    while True:
        add_addr=(input('Enter single ip addres or multiple(separated by commas): ')).split(',')
        ticket=input('Enter the number of ticket: ')
        if add_addr[0] == '':
            print('You need to enter at least one IP address')
        else:
            break
    #time.sleep(10)
    values=getalldacl()
    for dacl_name,dacl_id in values.items():
        if 'VPN-Konev' in dacl_name:
            current_content=get_content(get_by_id(dacl_id))
            content = add_content(current_content,add_addr,ticket=ticket,dacl_name=dacl_name)
            uniq_content = uniq_content_verif(content)
            put_content(dacl_name,dacl_id,uniq_content)



