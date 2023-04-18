# -*- coding: utf-8 -*-
"""
Задание 12.3

Создать функцию print_ip_table, которая отображает таблицу доступных
и недоступных IP-адресов.

Функция ожидает как аргументы два списка:
* список доступных IP-адресов
* список недоступных IP-адресов

Результат работы функции - вывод на стандартный поток вывода таблицы вида:

Reachable    Unreachable
-----------  -------------
10.1.1.1     10.1.1.7
10.1.1.2     10.1.1.8
             10.1.1.9

"""
from task_12_1 import ping_ip_addresses
from tabulate import tabulate
ip_list=['8.8.8.8','8.8.4.4','192.168.1.1']
col=['Reachable','Unreachable']
#u_l = [10.1.1.7, 10.1.1.8, 10.1.1.9]
#r_l = [10.1.1.1,10.1.1.2]

def print_ip_table(r_l,u_l):
    dict1={}
    dict1['Reachable']=r_l
    dict1['Unreachable']=u_l
    print(tabulate(dict1, headers='keys')) 

r_l,u_l=ping_ip_addresses(ip_list)
#print(dict0)
print_ip_table(r_l,u_l)
