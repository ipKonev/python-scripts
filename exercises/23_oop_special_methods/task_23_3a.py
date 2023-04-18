# -*- coding: utf-8 -*-

"""
Задание 23.3a

В этом задании надо сделать так, чтобы экземпляры класса Topology
были итерируемыми объектами.
Основу класса Topology можно взять из любого задания 22.1x или задания 23.3.

После создания экземпляра класса, экземпляр должен работать как итерируемый объект.
На каждой итерации должен возвращаться кортеж, который описывает одно соединение.
Порядок вывода соединений может быть любым.


Пример работы класса:

In [1]: top = Topology(topology_example)

In [2]: for link in top:
   ...:     print(link)
   ...:
(('R1', 'Eth0/0'), ('SW1', 'Eth0/1'))
(('R2', 'Eth0/0'), ('SW1', 'Eth0/2'))
(('R2', 'Eth0/1'), ('SW2', 'Eth0/11'))
(('R3', 'Eth0/0'), ('SW1', 'Eth0/3'))
(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))
(('R3', 'Eth0/2'), ('R5', 'Eth0/0'))


Проверить работу класса.
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

    def __add__(self,other):
        new=self.topology.copy()
        new.update(other.topology)
        return Topology(new)

    def __iter__(self):
        return iter(self.topology.items())

#pprint(topolog.add_link(('R1', 'Eth0/1'), ('R7', 'Eth0/0')))
#pprint(topolog.add_link(('R1', 'Eth0/2'), ('R8', 'Eth0/0')))
#pprint(topolog.topology)
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

topology_example2 = {
    ("R1", "Eth0/4"): ("R7", "Eth0/0"),
    ("R1", "Eth0/6"): ("R9", "Eth0/0"),
}
if __name__ == '__main__':
    topo1=Topology(topology_example)
    topo2=Topology(topology_example)
    #topo3=topo1+topo2
    #pprint(topo3)
