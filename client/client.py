import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from imports.config import *
from vm_detection import *
from get_cve import *
from get_ip import *

def send_vuln_report(vuln_data):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    message = ""
    is_vm_flag = False

    if is_vm():  
        message = f"[!] Error: The system is running in a virtual machine."
        is_vm_flag = True

    data_to_send = {
        "vuln_data": vuln_data,
        "message": message,
        "is_vm": is_vm_flag
    }
    with socket.create_connection((SERVER_IP, PORT)) as sock:
        with context.wrap_socket(sock, server_hostname=SERVER_IP) as secure_sock:
            secure_sock.sendall(json.dumps(data_to_send).encode('utf-8'))

if __name__ == "__main__":
    target_ip = "192.168.56.101"
    try:
        cve_list = get_cve(target_ip)
        send_vuln_report(cve_list)

    except KeyboardInterrupt:
        exit(1)
