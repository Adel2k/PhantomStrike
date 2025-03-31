import socket
import ssl
from get_cve import *
from vm_detection import *
import json

SERVER_IP = "localhost"
PORT = 1234
CERTFILE = "server.crt"
def send_vuln_report(vuln_data):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE  # Disable SSL verification for testing

    with socket.create_connection((SERVER_IP, PORT)) as sock:
        with context.wrap_socket(sock, server_hostname=SERVER_IP) as secure_sock:
            secure_sock.sendall(json.dumps(vuln_data).encode('utf-8'))  # ✅ FIXED: Convert list to JSON before encoding
            print("[+] Sent vulnerability data")


if __name__ == "__main__":
    target_ip = "192.168.56.101"

    if is_vm():
        print("The system is running in a virtual machine.")
        exit(1)
    
    # nmap_output = subprocess.run(["nmap", "-O", target_ip], capture_output=True, text=True)
    
    # os_info = "Unknown"

    # for line in nmap_output.stdout.split("\n"):
    #     if "OS details:" in line:
            # os_info = line.split(":", 1)[1].strip()

    # print(f"Detected OS: {os_info}")
    
    cve_list = get_cve(target_ip)
    # if cve_list:
    #     for cve in cve_list:
    #         cve = cve["cve"]
    #         print(f"Searching for exploits for {cve}...")

    send_vuln_report(cve_list)
