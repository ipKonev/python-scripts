# -*- coding: utf-8 -*-
"""
Задание 15.4

Создать функцию get_ints_without_description, которая ожидает как аргумент
имя файла, в котором находится конфигурация устройства.


Функция должна обрабатывать конфигурацию и возвращать список имен интерфейсов,
на которых нет описания (команды description).

Пример интерфейса с описанием:
interface Ethernet0/2
 description To P_r9 Ethernet0/2
 ip address 10.0.19.1 255.255.255.0
 mpls traffic-eng tunnels
 ip rsvp bandwidth

Интерфейс без описания:
interface Loopback0
 ip address 10.1.1.1 255.255.255.255

Проверить работу функции на примере файла config_r1.txt.
"""
import re

regex=re.compile(
        r'\ninterface (?P<intf>\S+)\n'
        r' (?P<description>description .*)*'
)

def  get_ints_without_description(fname):
    list1=[]
    with open(fname) as f:
        for m in regex.findall(f.read()):
            if not m[1]:
                list1.append(m[0])
    return list1

print(get_ints_without_description('config_r1.txt'))
