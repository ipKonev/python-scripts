# -*- coding: utf-8 -*-
"""
Задание 6.2b

Сделать копию скрипта задания 6.2a.

Дополнить скрипт: Если адрес был введен неправильно, запросить адрес снова.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
while True:
    a=input('Enter ip: ')
    b=a.split('.')
    valid = len(b) == 4

    for i in b:
        valid = i.isdigit() and int(i) in range(256) and valid
    if valid:
        break
    print('Неправильный IP-адрес')



b=[int(i) for i in b]
if b[0]==b[1]==b[2]==b[3]==255:
    print('local broadcast')

elif b[0]==b[1]==b[2]==b[3]==0:
    print('unassigned')

elif b[0] not in range(1,224):
    if b[0] in range(224,240):
        print('multicast')
    else:
        print('unused')
else:
    print('unicast')
