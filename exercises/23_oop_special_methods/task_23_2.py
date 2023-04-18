# -*- coding: utf-8 -*-

"""
Задание 23.2

Скопировать класс CiscoTelnet из любого задания 22.2x и добавить классу поддержку
работы в менеджере контекста.
При выходе из блока менеджера контекста должно закрываться соединение.

Пример работы:

In [14]: r1_params = {
    ...:     'ip': '192.168.100.1',
    ...:     'username': 'cisco',
    ...:     'password': 'cisco',
    ...:     'secret': 'cisco'}

In [15]: from task_23_2 import CiscoTelnet

In [16]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:
sh clock
*19:17:20.244 UTC Sat Apr 6 2019
R1#

In [17]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:     raise ValueError('Возникла ошибка')
    ...:
sh clock
*19:17:38.828 UTC Sat Apr 6 2019
R1#
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-17-f3141be7c129> in <module>
      1 with CiscoTelnet(**r1_params) as r1:
      2     print(r1.send_show_command('sh clock'))
----> 3     raise ValueError('Возникла ошибка')
      4

ValueError: Возникла ошибка
"""
import time
import re
import telnetlib
from pprint import pprint
from textfsm import clitable
class CiscoTelnet:
    def __init__(self,ip,username,password,secret):
        self.ip=ip
        self.telnet=telnetlib.Telnet(ip)
        self.telnet.read_until(b'Username:')
        self._write_line(username)
        self.telnet.read_until(b'Password:')
        self._write_line(password)
        self._write_line('enable')
        self.telnet.read_until(b'Password:')
        self._write_line(secret)
        self._write_line('terminal length 0')
        time.sleep(1)
        self.telnet.read_very_eager()

    def _write_line(self,line):
        self.telnet.write(line.encode('ascii') + b'\n')

    def send_show_command(self,command,parse=True,templates='templates',index='index'):
        self._write_line(command)
        time.sleep(1)
        output=self.telnet.read_very_eager().decode('ascii')
        return output
        '''if not parse:
            return output
        elif parse:
            list1=[]
            cli_table=clitable.CliTable(index,templates)
            attributes={'Command': command}
            cli_table.ParseCmd(output,attributes)
            header=list(cli_table.header)
            data_rows=[list(row) for row in cli_table]
            for row in data_rows:
                dict2=dict(zip(header,row))
                list1.append(dict2)
            return list1'''
    def send_config_commands(self,command,strict=True):
        output=''
        if isinstance(command,str):
            command=[command]
        self._write_line('conf t')
        for cmd in command:
            self._write_line(cmd)
            time.sleep(1)
            result=self.telnet.read_very_eager().decode('ascii')
            output+=result
            self._error_in_command(cmd,result,strict=strict)
        self._write_line('end')
        time.sleep(1)
        output+=self.telnet.read_very_eager().decode('ascii')
        return output

    def _error_in_command(self,command,result,strict):
        regex = '% (?P<error>.+)'
        template = ('При выполнении команды "{}" на устройстве {} '
                    'возникла ошибка -> {}')
        match=re.search(regex,result)
        if match:
            message=template.format(command,self.ip,match.group('error'))
            if strict:
                raise ValueError(message)
            else:
                print(message)
    def __enter__(self):
        return self
    def __exit__(self,exc_type,exc_value,traceback):
        self.telnet.close()

if __name__ == '__main__':
    r1=CiscoTelnet('192.168.100.1','cisco','cisco','cisco')
    r1.send_show_command('sh ip int br')
    r1.send_config_commands('logging 10.1.1.1')
