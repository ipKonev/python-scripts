# -*- coding: utf-8 -*-
"""
Задание 7.1

Обработать строки из файла ospf.txt и вывести информацию по каждой строке в таком
виде на стандартный поток вывода:

Prefix                10.0.24.0/24
AD/Metric             110/41
Next-Hop              10.0.13.3
Last update           3d18h
Outbound Interface    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

O        10.0.79.0/24 [110/20] via 10.0.19.9, 4d02h, FastEthernet0/2
"""
with open('ospf.txt') as f:
    for line in f:
        __,pfx,metric,__,nhop,upd,outf=line.split()
        print(f'''Prefix                {pfx}
AD/Metric             {metric.strip('[]')}
Next-Hop              {nhop.strip(',')}
Last update           {upd.strip(',')}
Outbound Interface    {outf}
''')
