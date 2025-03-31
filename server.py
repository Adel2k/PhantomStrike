import socket
import ssl
import threading
import sqlite3
import json

HOST = "0.0.0.0"
PORT = 1234
CERTFILE = "server.crt" 
KEYFILE = "server.key"

DB_NAME = "vuln_reports.db"

def init_db():
    """Creates the database and vulnerability reports table if not exists."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            report TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_report(ip, report):
    """Saves the vulnerability report to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reports (ip, report) VALUES (?, ?)", (ip, report))
    conn.commit()
    conn.close()
    print(f"[✔] Report saved from {ip}")

def handle_client(client_socket, addr):
    """Handles incoming client connections securely."""
    try:
        data = client_socket.recv(4096).decode().strip()
        if data:
            print(f"[!] Received report from {addr[0]}: {data}")
            save_report(addr[0], data)
    except Exception as e:
        print(f"[Error] {e}")
    finally:
        client_socket.close()

def start_server():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)

    with socket.create_server((HOST, PORT)) as server_socket:
        with context.wrap_socket(server_socket, server_side=True) as secure_socket:
            print(f"[*] Secure Server listening on {HOST}:{PORT}...")

            while True:
                client_socket, client_address = secure_socket.accept()
                print(f"[+] Connection from {client_address}")

                with client_socket:
                    data = client_socket.recv(4096).decode('utf-8')  # ✅ Decode received bytes
                    try:
                        vuln_list = json.loads(data)  # ✅ Convert JSON string to Python list
                        print("[!] Received vulnerability report:")
                        for vuln in vuln_list:
                            if isinstance(vuln, dict) and 'CVE' in vuln:  # ✅ Ensure correct structure
                                print(f" - {vuln['CVE']} | {vuln['Severity']} | {vuln['Description']}")
                            else:
                                print("[!] Warning: Invalid vulnerability data format.")
                        print(vuln_list)
                    except json.JSONDecodeError:
                        print("[!] Error: Received invalid JSON data")


if __name__ == "__main__":
    start_server()
