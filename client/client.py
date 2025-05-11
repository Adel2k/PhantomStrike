import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from client.vm_detection import *
from client.get_cve import *
from client.install import *
import ssl
import socket
import json



def send_vuln_report(vuln_data):
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        message = ""
        is_vm_flag = False
    
    except KeyboardInterrupt:
        sys.exit(1)

    except TimeoutError:
        sys.exit(1)

    except Exception as e:
        sys.exit(1) 

    if is_vm():  
        message = f"[!] Error: The system is running in a virtual machine."
        is_vm_flag = True

    data_to_send = {
        "vuln_data": vuln_data,
        "message": message,
        "is_vm": is_vm_flag
    }
    with socket.create_connection(("localhost", 1234)) as sock:
        with context.wrap_socket(sock, server_hostname="10.19.248.157") as secure_sock:
            secure_sock.sendall(json.dumps(data_to_send).encode('utf-8'))

def sent_score():
    target_ip = "localhost"
    try:
        cve_list = get_cve(target_ip)
        send_vuln_report(cve_list)

    except KeyboardInterrupt:
        sys.exit(1)

    except TimeoutError:
        sys.exit(1)

    except Exception as e:
        sys.exit(1)