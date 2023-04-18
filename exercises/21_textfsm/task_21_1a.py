# -*- coding: utf-8 -*-
"""
Задание 21.1a

Создать функцию parse_output_to_dict.

Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM.
  Например, templates/sh_ip_int_br.template
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список словарей:
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на выводе команды output/sh_ip_int_br.txt
и шаблоне templates/sh_ip_int_br.template.
"""
from pprint import pprint
from task_21_1 import parse_command_output
def parse_output_to_dict(template,command_output):
    dict_list=[]
    b=parse_command_output(template,command_output)
    keys,values=b[0],b[1:]
    for each in values:
        dict1=dict(zip(keys,each))
        dict_list.append(dict1)
    return dict_list


if __name__=='__main__':
    out=open('output/sh_ip_int_br.txt').read()
    tmp='templates/sh_ip_int_br.template'
    pprint(parse_output_to_dict(tmp,out))
