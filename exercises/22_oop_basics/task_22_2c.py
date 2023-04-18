# -*- coding: utf-8 -*-

"""
Задание 22.2c

Скопировать класс CiscoTelnet из задания 22.2b и изменить метод send_config_commands
добавив проверку команд на ошибки.

У метода send_config_commands должен быть дополнительный параметр strict:
* strict=True значит, что при обнаружении ошибки, необходимо сгенерировать
  исключение ValueError (значение по умолчанию)
* strict=False значит, что при обнаружении ошибки, надо только вывести
  на стандартный поток вывода сообщене об ошибке

Метод дожен возвращать вывод аналогичный методу send_config_set
у netmiko (пример вывода ниже). Текст исключения и ошибки в примере ниже.

Пример создания экземпляра класса:
In [1]: from task_22_2c import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

In [4]: commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
In [5]: correct_commands = ['logging buffered 20010', 'ip http server']
In [6]: commands = commands_with_errors+correct_commands

Использование метода send_config_commands:

In [7]: print(r1.send_config_commands(commands, strict=False))
При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.
При выполнении команды "logging" на устройстве 192.168.100.1 возникла ошибка -> Incomplete command.
При выполнении команды "a" на устройстве 192.168.100.1 возникла ошибка -> Ambiguous command:  "a"
conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#a
% Ambiguous command:  "a"
R1(config)#logging buffered 20010
R1(config)#ip http server
R1(config)#end
R1#

In [8]: print(r1.send_config_commands(commands, strict=True))
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-8-0abc1ed8602e> in <module>
----> 1 print(r1.send_config_commands(commands, strict=True))

...

ValueError: При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.

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
        if not parse:
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
            return list1

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

if __name__ == '__main__':
    r1=CiscoTelnet('192.168.100.1','cisco','cisco','cisco')
    r1.send_show_command('sh ip int br')
    r1.send_config_commands('logging 10.1.1.1')
