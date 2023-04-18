# -*- coding: utf-8 -*-
"""
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте команду ping.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
import subprocess

def ping_ip_addresses(ip_list):
    a_l,u_l =[],[]
    for ip in ip_list:
        reply=subprocess.run(['ping', '-c', '3', '-n', ip],
                             stdout=subprocess.DEVNULL)
        if reply.returncode != 0:
            u_l.append(ip)
        else:
            a_l.append(ip)
    return a_l,u_l

ip_list=['8.8.8.8','8.8.4.4','192.168.1.1']

if __name__ == '__main__':
    print(ping_ip_addresses(ip_list))
