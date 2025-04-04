import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from imports.config import *

def get_ip_address():
    os_name = platform.system().lower()
    ip_address = None

    try:
        if os_name == "linux":
            result = subprocess.check_output("ip a", shell=True).decode()
            match = re.search(r"inet\s+([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", result)
            if match:
                ip_address = match.group(1)
        elif os_name == "windows":
            result = subprocess.check_output("ipconfig", shell=True).decode()
            match = re.search(r"IPv4 Address[^\n]*:\s*([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", result)
            if match:
                ip_address = match.group(1)
        else:
            print("Unsupported OS")
        
        return ip_address if ip_address else "IP not found"

    except subprocess.CalledProcessError:
        return None
