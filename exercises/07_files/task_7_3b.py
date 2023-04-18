# -*- coding: utf-8 -*-
"""
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Переделать скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Пример работы скрипта:

Enter VLAN number: 10
10       0a1b.1c80.7000      Gi0/4
10       01ab.c5d0.70d0      Gi0/8

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
a=input('Enter vlan num: ')
with open('CAM_table.txt') as f:
    result=[]
    for line in f:
        line=line.strip().split()
        #print(line[0],a)
        if len(line) and line[0].isdigit() and line[0] == a: 
            vlan,mac,__,intf = line
            list1=[int(vlan),mac,intf]
            #result.append(list1)
            print(f'{vlan:8} {mac:16} {intf}')
        else:
            pass
