import subprocess

def execute_exploit(cve: str, target_ip: str):
    exploit_command = f"python3 ./exploits/{cve}.py {target_ip}"
    try:
        subprocess.run(exploit_command, shell=True, check=True)
        print(f"Exploit for {cve} executed successfully on {target_ip}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing exploit for {cve}: {e}")
