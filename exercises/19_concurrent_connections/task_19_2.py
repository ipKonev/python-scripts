# -*- coding: utf-8 -*-
"""
Задание 19.2

Создать функцию send_show_command_to_devices, которая отправляет одну и ту же
команду show на разные устройства в параллельных потоках, а затем записывает
вывод команд в файл. Вывод с устройств в файле может быть в любом порядке.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* command - команда
* filename - имя текстового файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в обычный текстовый файл в таком формате
(перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.2   YES NVRAM  up                    up
Ethernet0/1                10.1.1.1        YES NVRAM  administratively down down
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml
"""
from itertools import repeat
import yaml
from concurrent.futures import ThreadPoolExecutor
from netmiko import ConnectHandler
cmd='show ip int br'
def send_cmd_operation(dev,command):
    with ConnectHandler(**dev) as ssh:
        ssh.enable()
        operation=ssh.send_command(command)
        prompt=ssh.find_prompt()
    return f'{prompt}{command}\n{operation}\n'

def send_show_command_to_devices(devices,command,filename,limit=3):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        result=executor.map(send_cmd_operation,devices,repeat(command))
    with open(filename,'w') as dst:
        for i in result:
            dst.write(i)

a=yaml.safe_load(open('devices.yaml'))
send_show_command_to_devices(a,cmd,'new.txt')
