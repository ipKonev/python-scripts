# -*- coding: utf-8 -*-
"""
Задание 15.5

Создать функцию generate_description_from_cdp, которая ожидает как аргумент
имя файла, в котором находится вывод команды show cdp neighbors.

Функция должна обрабатывать вывод команды show cdp neighbors и генерировать
на основании вывода команды описание для интерфейсов.

Например, если у R1 такой вывод команды:
R1>show cdp neighbors
Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater

Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
SW1              Eth 0/0           140          S I      WS-C3750-  Eth 0/1

Для интерфейса Eth 0/0 надо сгенерировать такое описание
description Connected to SW1 port Eth 0/1

Функция должна возвращать словарь, в котором ключи - имена интерфейсов,
а значения - команда задающая описание интерфейса:
'Eth 0/0': 'description Connected to SW1 port Eth 0/1'


Проверить работу функции на файле sh_cdp_n_sw1.txt.
"""
import re

regex=re.compile(
    r'(?P<dev>\S+\d+)\s+'
    r'(?P<l_intf>\S+ \S+) '
    r'.*'
    r' (?P<n_intf>\S+ \S+)'
)
def generate_description_from_cdp(fname):
    dict1={}
    with open(fname) as f:
        for m in regex.findall(f.read()):
            dict1[m[1]]=f'description Connected to {m[0]} port {m[2]}'

    return dict1

print(generate_description_from_cdp('sh_cdp_n_sw1.txt'))
