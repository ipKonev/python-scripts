# -*- coding: utf-8 -*-

"""
Задание 22.1c

Изменить класс Topology из задания 22.1b.

Добавить метод delete_node, который удаляет все соединения с указаным устройством.

Если такого устройства нет, выводится сообщение "Такого устройства нет".

Создание топологии
In [1]: t = Topology(topology_example)

In [2]: t.topology
Out[2]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Удаление устройства:
In [3]: t.delete_node('SW1')

In [4]: t.topology
Out[4]:
{('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Если такого устройства нет, выводится сообщение:
In [5]: t.delete_node('SW1')
Такого устройства нет

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
    def delete_node(self,node):
        #print(self.topology.keys())
        removal=[]
        for key,value in self.topology.items():
            l_dev,l_intf=key
            r_dev,r_intf=value
            if l_dev==node:
                removal.append(key)
            elif r_dev==node:
                removal.append(key)
        if removal:
            for each in removal:
                self.topology.pop(each)
            #print(removal)
        else:
            print('Такого устройства нет')

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
#pprint(topolog.topology)
#pprint(topolog.delete_link(('R5', 'Eth0/0'), ('R3', 'Eth0/2')))
#pprint(topolog.topology)
pprint(topolog.delete_node('SW1'))

#pprint(topolog.topology)
