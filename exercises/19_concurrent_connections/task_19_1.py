# -*- coding: utf-8 -*-
"""
Задание 19.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции ping_ip_addresses:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.

Подсказка о работе с concurrent.futures:
Если необходимо пинговать несколько IP-адресов в разных потоках,
надо создать функцию, которая будет пинговать один IP-адрес,
а затем запустить эту функцию в разных потоках для разных
IP-адресов с помощью concurrent.futures (это надо сделать в функции ping_ip_addresses).
"""
import subprocess
from concurrent.futures import ThreadPoolExecutor

list1=['8.8.8.8','192.168.100.1','192.168.1.1','192.168.1.2']
def operation(addr):
    ping=subprocess.run(['ping','-c','3', addr],stdout=subprocess.DEVNULL)
    return ping.returncode,addr

def ping_ip_addresses(ip_list,limit=3):
    a_l,u_l=[],[]
    with ThreadPoolExecutor(max_workers=limit) as executor:
        result=executor.map(operation,ip_list)
    for i in result:
        if i[0]==0:
            a_l.append(i[1])
        else:
            u_l.append(i[1])
    return a_l, u_l

print(ping_ip_addresses(list1))
