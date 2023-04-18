# -*- coding: utf-8 -*-
"""
Задание 21.4

Создать функцию send_and_parse_show_command.

Параметры функции:
* device_dict - словарь с параметрами подключения к одному устройству
* command - команда, которую надо выполнить
* templates_path - путь к каталогу с шаблонами TextFSM
* index - имя индекс файла, значение по умолчанию "index"

Функция должна подключаться к одному устройству, отправлять команду show
с помощью netmiko, а затем парсить вывод команды с помощью TextFSM.

Функция должна возвращать список словарей с результатами обработки
вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br
и устройствах из devices.yaml.
"""
from textfsm import clitable
from netmiko import ConnectHandler
from pprint import pprint
import yaml

def send_and_parse_show_command(device_dict,command,templates_path,index='index'):
    attributes={'Command': command}
    dict_list=[]
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        output=ssh.send_command(command)
    cli_table=clitable.CliTable(index,templates_path)
    cli_table.ParseCmd(output,attributes)
    header=cli_table.header
    data_rows=[list(row) for row in cli_table]
    for each in data_rows:
        dict1=dict(zip(header,each))
        dict_list.append(dict1)

    return dict_list


if __name__=='__main__':
    dict1=yaml.safe_load(open('devices.yaml'))[0]
    command='sh ip int br'
    templates_path='templates'
    pprint(send_and_parse_show_command(dict1,command,templates_path))
