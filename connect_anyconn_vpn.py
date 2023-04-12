import iperf3
import sys
import os
import keyring
import click
import pexpect
from pprint import pprint
from pyzabbix import ZabbixMetric, ZabbixSender
import time
import socket
import subprocess
import yaml

def connect_vpn(VPN_HOST, VPN_BIN, USERNAME, VPN_PASS):

    child = pexpect.spawn(VPN_BIN + ' -s connect ' + VPN_HOST, encoding='utf-8')
    child.expect(r'Username: \[.*\]')
    child.sendline(USERNAME)
    child.expect('Password:')   
    child.sendline(VPN_PASS)
    child.expect('  >> state: Connected')
    print('connected')



def stop_vpn():
    stop = subprocess.run("/opt/cisco/anyconnect/bin/vpn disconnect", shell=True, encoding='utf-8', stdout=subprocess.DEVNULL)

def kill_hanging_py():
    #stop = subprocess.run('kill -9 $(pgrep python3.8)', shell=True)        
    return subprocess.run( f'kill -9 {os.getpid()}', shell=True)     

def resolve_hostnames(ise_name, ise_addr):
    return 1 if socket.gethostbyname(ise_name) == ise_addr else 0


def iperf_test(iperf_server, 
                server_port = '5201',
                duration = 5,
                blksize = 1300,):
    client = iperf3.Client()
    client.duration = duration
    client.server_hostname = iperf_server
    client.port = server_port
    client.blksize = blksize
    client.reverse = True
    result = client.run()
    return int(f'{round(result.sent_Mbps)}')

def scan_port(ip, port):
    scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scanner.settimeout(1)
    try:
        connect = scanner.connect((ip, port))
        return 1
    except:
        return 0
    finally:
        scanner.close()

def collect_info(VPN_HOST, ISE_NODE1_NAME, ISE_NODE1_ADDR, ISE_NODE2_NAME, ISE_NODE2_ADDR, IPERF_SERVER):
    result_data = {}
    result_data['host'] = VPN_HOST.split('/')[2]
    result_data['ise1_name_resolved'] = resolve_hostnames(
                                        ISE_NODE1_NAME,
                                        ISE_NODE1_ADDR)
    result_data['ise2_name_resolved'] = resolve_hostnames(
                                        ISE_NODE2_NAME,
                                        ISE_NODE2_ADDR)
    result_data['upload_speed'] = iperf_test(IPERF_SERVER) 
    result_data['ise1_port_is_opened'] = scan_port(ISE_NODE1_ADDR, 8443)
    result_data['ise2_port_is_opened'] = scan_port(ISE_NODE2_ADDR, 8443)
    return result_data


def send_to_zabbix(result_datai, ZABBIX_PROXY):
    metrics = []
    for key, value in result_data.items():
        metric = ZabbixMetric(result_data['host'], key, value)
        metrics.append(metric)
    zbx = ZabbixSender(ZABBIX_PROXY)
    zbx.send(metrics)


if __name__ == '__main__':    
    with open('/root/vpn-monitoring/url.yaml') as f:
        data = yaml.safe_load(f)
    stop_vpn()
    VPN_HOSTS = data['VPN_HOSTS']
    for VPN_HOST in VPN_HOSTS:    
        #print(VPN_HOST)
        connect_vpn(VPN_HOST, data['VPN_BIN'],data['USERNAME'],data['VPN_PASS'])
        result_data = collect_info(VPN_HOST, data['ISE_NODE1_NAME'], data['ISE_NODE1_ADDR'], data['ISE_NODE2_NAME'], data['ISE_NODE2_ADDR'], data['IPERF_SERVER'])
        pprint(result_data)
        send_to_zabbix(result_data, data['ZABBIX_PROXY'])
        stop_vpn()
    kill_hanging_py()
