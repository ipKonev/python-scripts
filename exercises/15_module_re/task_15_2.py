# -*- coding: utf-8 -*-
"""
Задание 15.2

Создать функцию parse_sh_ip_int_br, которая ожидает как аргумент
имя файла, в котором находится вывод команды show ip int br

Функция должна обрабатывать вывод команды show ip int br и возвращать такие поля:
* Interface
* IP-Address
* Status
* Protocol

Информация должна возвращаться в виде списка кортежей:
[('FastEthernet0/0', '10.0.1.1', 'up', 'up'),
 ('FastEthernet0/1', '10.0.2.1', 'up', 'up'),
 ('FastEthernet0/2', 'unassigned', 'down', 'down')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла sh_ip_int_br.txt.
FastEthernet0/0            15.0.15.1       YES manual up                    up
"""
import re
regex=re.compile(
    r'(?P<intf>\S+)\s+'
    r'(?P<addr>[\d.]+|unassigned)\s+'
    r'\w+ \w+\s+'
    r'(?P<ls>up|down|administratively\s+down)\s+'
    r'(?P<proto>up|down)'
)
def parse_sh_ip_int_br(fname):
    with open(fname) as f:
        match=regex.findall(f.read())
        m=[i for i in match]

    return m
print(parse_sh_ip_int_br('sh_ip_int_br.txt'))
