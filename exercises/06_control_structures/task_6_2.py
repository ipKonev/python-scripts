# -*- coding: utf-8 -*-
"""
Задание 6.2

Запросить у пользователя ввод IP-адреса в формате 10.0.1.1
В зависимости от типа адреса (описаны ниже), вывести на стандартный поток вывода:
   'unicast' - если первый байт в диапазоне 1-223
   'multicast' - если первый байт в диапазоне 224-239
   'local broadcast' - если IP-адрес равен 255.255.255.255
   'unassigned' - если IP-адрес равен 0.0.0.0
   'unused' - во всех остальных случаях

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
a=[int(i) for i in input('Enter ip: ').split('.')]

if a[0]==a[1]==a[2]==a[3]==255:
    print('local broadcast')

elif a[0]==a[1]==a[2]==a[3]==0:
    print('unassigned')

elif a[0] not in range(1,224):
    if a[0] in range(224,240):
        print('multicast')
    else:
        print('unused')
else:
    print('unicast')
