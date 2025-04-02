import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from imports.config import *

import mysql.connector
def save_db(ip, report):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="your_user",
            password="your_password",
            database="your_database"
        )
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS reports (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ip VARCHAR(45),  -- IPv6 compatible
            report JSON       -- Store the JSON data
        )''')

        cursor.execute("INSERT INTO reports (ip, report) VALUES (%s, %s)", (ip, report))

        conn.commit()
        print("Data inserted into MySQL successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def save_report(ip, report):
    with open(REPORT_FILE, "a") as file:
        file.write(f"[✔] Report from {ip}\n")
        file.write(report + "\n\n")
    print(f"[✔] Report saved from {ip}")

def start_server():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)

    with socket.create_server((HOST, PORT)) as server_socket:
        with context.wrap_socket(server_socket, server_side=True) as secure_socket:
            print(f"{GREEN}{BOLD}Secure Server listening on {RESET}{HOST}:{PORT}...")

            while True:
                client_socket, client_address = secure_socket.accept()
                print(f"{GREEN}[+] Connection from {client_address}{RESET}")

                with client_socket:
                    data = client_socket.recv(4096).decode('utf-8').strip()
                    if data:
                        try:
                            received_data = json.loads(data)
                            vuln_data = received_data.get("vuln_data", [])
                            message = received_data.get("message", "No message")
                            is_vm = received_data.get("is_vm", False)

                            print(f"{YELLOW}[+] Received vulnerability report:{RESET}")
                            for vuln in vuln_data:
                                if isinstance(vuln, dict) and 'CVE' in vuln:
                                    print(f" - {vuln['CVE']} | {vuln.get('Severity', 'N/A')} | "
                                        f"{vuln.get('Description', 'No description')}")
                                else:
                                    print(f"{MAGENTA}[!] Warning: Invalid vulnerability data format.{RESET}")

                            print(f"{CYAN}[+] Message from client: {message}{RESET}")
                            
                            if is_vm:
                                print(f"{RED}[!] Target system is a virtual machine!{RESET}")
                            
                            save_db(client_address[0], json.dumps(received_data))
                            save_report(client_address[0], json.dumps(received_data))

                        except json.JSONDecodeError:
                            print(f"{RED}[!] Error: Received invalid JSON data{RESET}")


if __name__ == "__main__":
    try:
        start_server()

    except KeyboardInterrupt:
        print(f"{RED}[!]End of the server{RESET}")