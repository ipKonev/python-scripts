# -*- coding: utf-8 -*-

"""
Задание 22.1b

Изменить класс Topology из задания 22.1a или 22.1.

Добавить метод delete_link, который удаляет указанное соединение.
Метод должен удалять и "обратное" соединение, если оно есть (ниже пример).

Если такого соединения нет, выводится сообщение "Такого соединения нет".

Создание топологии
In [7]: t = Topology(topology_example)

In [8]: t.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Удаление линка:
In [9]: t.delete_link(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Удаление "обратного" линка:
в словаре есть запись ``('R3', 'Eth0/2'): ('R5', 'Eth0/0')``, но вызов delete_link
с указанием ключа и значения в обратном порядке, должно удалять соединение:

In [11]: t.delete_link(('R5', 'Eth0/0'), ('R3', 'Eth0/2'))

In [12]: t.topology
Out[12]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3')}

Если такого соединения нет, выводится сообщение:
In [13]: t.delete_link(('R5', 'Eth0/0'), ('R3', 'Eth0/2'))
Такого соединения нет

"""
from pprint import pprint

class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)
    def _normalize(self,topo):
        list1=[]
        for k,v in topo.items():
            elem=[k,v]
            relem=[v,k]
            if relem not in list1:
                list1.append(elem)
            else:
                pass
        return dict(list1)
    def delete_link(self,t1,t2):
        if not self.topology.get(t1) and not self.topology.get(t2):
            print('Такого соединения нет')
        elif self.topology.get(t1):
            self.topology.pop(t1)
        elif self.topology.get(t2):
            self.topology.pop(t2)


topology_example = {
    ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
    ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
    ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
    ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
    ("R3", "Eth0/1"): ("R4", "Eth0/0"),
    ("R3", "Eth0/2"): ("R5", "Eth0/0"),
    ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
    ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
    ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
}
topolog=Topology(topology_example)
pprint(topolog.topology)
pprint(topolog.delete_link(('R5', 'Eth0/0'), ('R3', 'Eth0/2')))
pprint(topolog.topology)
