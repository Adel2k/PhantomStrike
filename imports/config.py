import os
import json
import socket
import ssl
import sqlite3
import nmap
import subprocess
import platform
import re

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
RESET = "\033[0m"

BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_PURPLE = "\033[95m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"

BOLD = "\033[1m"
UNDERLINE = "\033[4m"
RESET = "\033[0m" 

from dotenv import load_dotenv
load_dotenv()

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CERTFILE = os.path.join(BASE_DIR, "server", "ssl", "server.crt")
KEYFILE = os.path.join(BASE_DIR, "server", "ssl", "server.key")
DB_NAME = os.getenv("DB_NAME")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")

SERVER_IP = os.getenv("SERVER_IP")
REPORT_FILE = "vuln_reports.txt"
VIRTUAL_GPUS = os.getenv("VIRTUAL_GPUS", "").split(",")
