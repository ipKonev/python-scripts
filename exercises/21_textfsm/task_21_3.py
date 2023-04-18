# -*- coding: utf-8 -*-
"""
Задание 21.3

Создать функцию parse_command_dynamic.

Параметры функции:
* command_output - вывод команды (строка)
* attributes_dict - словарь атрибутов, в котором находятся такие пары ключ-значение:
 * 'Command': команда
 * 'Vendor': вендор
* index_file - имя файла, где хранится соответствие между командами и шаблонами.
  Значение по умолчанию - "index"
* templ_path - каталог, где хранятся шаблоны. Значение по умолчанию - "templates"

Функция должна возвращать список словарей с результатами обработки
вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br.
"""
from pprint import pprint
from textfsm import clitable

def parse_command_dynamic(command_output,attributes_dict,index_file='index',templ_path='templates'):
    dict_list=[]
    cli_table=clitable.CliTable(index_file, templ_path)
    cli_table.ParseCmd(command_output,attributes_dict)
    header=list(cli_table.header)
    data_rows = [list(row) for row in cli_table]
    for each in data_rows:
        dict1=dict(zip(header,each))
        dict_list.append(dict1)
    return dict_list


if __name__=='__main__':
    output=open('output/sh_ip_int_br.txt').read()
    dict1={'Command': 'sh ip int br'}
    ifile='index'
    tpath='template'
    pprint(parse_command_dynamic(output,dict1))
