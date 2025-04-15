import os
import subprocess
import urllib.request
import time
import shutil
import sys

NMAP_DOWNLOAD_URL = "https://nmap.org/dist/nmap-7.94-setup.exe"
NMAP_INSTALL_PATH = r"C:\Program Files (x86)\Nmap\nmap.exe"

def is_nmap_installed():
    return os.path.exists(NMAP_INSTALL_PATH)

def download_nmap_installer(filename="nmap_installer.exe"):
    urllib.request.urlretrieve(NMAP_DOWNLOAD_URL, filename)
    return filename

def install_nmap(installer):
    subprocess.run([installer, "/S"], check=True)
    os.remove(installer)

def install():
    if not is_nmap_installed():
        installer = download_nmap_installer()
        install_nmap(installer)
        time.sleep(5)
    else:
        sys.exit(1)
