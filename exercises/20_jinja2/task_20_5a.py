# -*- coding: utf-8 -*-
"""
Задание 20.5a

Создать функцию configure_vpn, которая использует
шаблоны из задания 20.5 для настройки VPN на маршрутизаторах
на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству 1
* dst_device_params - словарь с параметрами подключения к устройству 2
* src_template - имя файла с шаблоном, который создает конфигурацию для строны 1
* dst_template - имя файла с шаблоном, который создает конфигурацию для строны 2
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов
и данных на каждом устройстве с помощью netmiko.
Функция возвращает кортеж с выводом команд с двух
маршрутизаторов (вывод, которые возвращает метод netmiko send_config_set).
Первый элемент кортежа - вывод с первого устройства (строка),
второй элемент кортежа - вывод со второго устройства.

При этом, в словаре data не указан номер интерфейса Tunnel,
который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel,
взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 5.
И надо будет настроить интерфейс Tunnel 5.

Для этого задания тест проверяет работу функции на первых двух устройствах
из файла devices.yaml. И проверяет, что в выводе есть команды настройки
интерфейсов, но при этом не проверяет настроенные номера тунелей и другие команды.
Они должны быть, но тест упрощен, чтобы было больше свободы выполнения.
"""
import yaml,re
from pprint import pprint
from netmiko import ConnectHandler
from task_20_5 import create_vpn_config
from datetime import time

data = {
    "tun_num": None,
    "wan_ip_1": "192.168.100.1",
    "wan_ip_2": "192.168.100.2",
    "tun_ip_1": "10.0.1.1 255.255.255.252",
    "tun_ip_2": "10.0.1.2 255.255.255.252",
}
data2 = {
                "tun_num": None,
                "wan_ip_1": "80.241.1.1",
                "wan_ip_2": "90.18.10.2",
                "tun_ip_1": "10.255.1.1 255.255.255.252",
                "tun_ip_2": "10.255.1.2 255.255.255.252",
            }

def tun_check(dev1,dev2,command='sh ip int br | i Tunnel'):
    list1=[]
    regex=r'\S+(?P<digit>\d) '
    with ConnectHandler(**dev1) as ssh:
        ssh.enable()
        output1=ssh.send_command(command)
    with ConnectHandler(**dev2) as ssh:
        ssh.enable()
        output2=ssh.send_command(command)
    if not output1 and not output2:
        return 0
    elif output1 or output2:
        for line in output1.split('\n'):
            match=re.search(regex,line)
            if match:
                list1.append(int(match.group('digit')))
        for line in output2.split('\n'):
            match=re.search(regex,line)
            if match:
                list1.append(int(match.group('digit')))

        return list(set(sorted(list1)))[-1]+1

def configure_vpn(src_device_params,dst_device_params,src_template,dst_template,vpn_data_dict):
    data['tun_num']=tun_check(src_device_params,dst_device_params)
    src,dst=create_vpn_config(src_template,dst_template,vpn_data_dict)
    src=src.split('\n')
    dst=dst.split('\n')
    with ConnectHandler(**src_device_params) as ssh:
        ssh.enable()
        output1=ssh.send_config_set(src)
    with ConnectHandler(**dst_device_params) as ssh:
        ssh.enable()
        output2=ssh.send_config_set(dst)
    return output1,output2

if __name__=='__main__':
    a=yaml.safe_load(open('devices.yaml'))
    dev1,dev2,*__=a
    template1='templates/gre_ipsec_vpn_1.txt'
    template2='templates/gre_ipsec_vpn_2.txt'
    pprint(configure_vpn(
        dev1,
        dev2,
        template1,
        template2,
        data))
