import iperf3
import os
from pprint import pprint
import socket
import subprocess
import time

def resolve_hostnames(ise_name, ise_addr):
    return socket.gethostbyname(ise_name) == ise_addr


def iperf_test(iperf_server = os.environ['IPERF_SERVER'],
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
    return f'{round(result.sent_Mbps, 2)} Mbit/s'

def scan_port(ip, port):
    scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scanner.settimeout(1)
    try:
        connect = scanner.connect((ip, port))
        return True
    except:
        return False
    finally:
        scanner.close()

def run_vpn(scriptname, password, username, addr):
    run = subprocess.run(f"/usr/bin/bash  {scriptname} '{password}' '{username}' {addr}", shell=True, encoding='utf-8')
    #time.sleep(3)
    return True if run.returncode == 0 else False

def stop_vpn():
    stop = subprocess.run('kill -9 $(pgrep openconnect)', shell=True)

def collect_info():
    result_data = {}
    result_data['ise1_name_resolved'] = resolve_hostnames(
                                        os.environ['ISE_NODE1_NAME'],
                                        os.environ['ISE_NODE1_ADDR'])
    result_data['ise2_name_resolved'] = resolve_hostnames(
                                        os.environ['ISE_NODE2_NAME'],
                                        os.environ['ISE_NODE2_ADDR'])
    result_data['upload_speed'] = iperf_test()
    result_data['ise1_port_is_opened'] = scan_port(os.environ['ISE_NODE1_NAME'], 8443)
    result_data['ise2_port_is_opened'] = scan_port(os.environ['ISE_NODE2_NAME'], 8443)
    return result_data

if __name__ == '__main__':
    data = collect_info() if run_vpn('vpn.sh',
                                    os.environ['VPN_GW_1_PASS'],
                                    os.environ['VPN_GW_1_UNAME'],
                                    os.environ['VPN_GW_1_ADDR']) == True else None
    stop_vpn()
    pprint(data)
