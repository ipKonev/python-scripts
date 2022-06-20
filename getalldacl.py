#Скрипт получает полный список dACL 
#Скрипт возвращает результат в виде словаря
#Где первый элемент Имя, а второй его id 
#значения для 'ERSADMIN','ERSPASS','ERSPATH' в переменном окружении

import os
from pprint import pprint
import requests
from requests.auth import HTTPBasicAuth
from requests.packages import urllib3

#Отключение предупреждения о недоверенном сертификате
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

if __name__ == '__main__':
    values=getalldacl()
    for k,v in values.items():
        if 'VPN-EXTERNAL' in k:
            print(k,v)

