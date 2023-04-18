# -*- coding: utf-8 -*-

"""
Задание 22.1d

Изменить класс Topology из задания 22.1c

Добавить метод add_link, который добавляет указанное соединение, если его еще
 нет в топологии.
Если соединение существует, вывести сообщение "Такое соединение существует",
Если одна из сторон есть в топологии, вывести сообщение
"Cоединение с одним из портов существует"


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

In [9]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [11]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
Такое соединение существует

In [12]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
Cоединение с одним из портов существует


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

    def add_link(self,t1,t2):
        for k,v in self.topology.items():
            if k==t1 and v==t2:
                print('Такое соединение существует')
                return None

        if t1 in self.topology.keys():
            print('Cоединение с одним из портов существует')
        elif t2 in self.topology.keys():
            print('Cоединение с одним из портов существует')
        else:
            self.topology[t1]=t2

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
#pprint(topolog.add_link('SW1'))

pprint(topolog.add_link(('R1', 'Eth0/1'), ('R7', 'Eth0/0')))
pprint(topolog.add_link(('R1', 'Eth0/2'), ('R8', 'Eth0/0')))
pprint(topolog.topology)
