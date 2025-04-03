lllllllllllllll = int
import os
import json
import socket
import ssl
import sqlite3
import nmap
import subprocess
import platform
import re

from os import getenv as lIlIllllIIIllI
from os.path import join as IllIIlIIllIlIl, dirname as IIIIlIllIIIlll, abspath as llIlllIIIIIllI
IIIIllIIIIIlIIIllI = '\x1b[31m'
llllIIllIllIlIIIII = '\x1b[32m'
IlIIlIlIlIlIIIlIlI = '\x1b[33m'
IlIlIIIIIIIIIIIIII = '\x1b[34m'
lIlIllIllllIIIIlll = '\x1b[35m'
llIIIIlIlllIIIllII = '\x1b[36m'
IIIIIlIIIllIIIIIlI = '\x1b[37m'
llllIIIIIlIlIIlIII = '\x1b[0m'
IIlIIIIIIIlIIIIIlI = '\x1b[90m'
IlIIIllIIlIIIllIlI = '\x1b[91m'
lIlIlIIlllllIIIIIl = '\x1b[92m'
IIlIllllllIIlIIIII = '\x1b[93m'
lIlllIIIIIIIIlIlll = '\x1b[94m'
IllIllIlllIIlIllII = '\x1b[95m'
llIlIIIIIlIIIlllIl = '\x1b[96m'
IlIllIIIIlllllIIII = '\x1b[97m'
lllIIlIlllllIIIlIl = '\x1b[1m'
IlIlllIlIlllllllIl = '\x1b[4m'
llllIIIIIlIlIIlIII = '\x1b[0m'
from dotenv import load_dotenv as lllllllIIIlIIl
lllllllIIIlIIl()
IIlllIIIIlllIlIlll = lIlIllllIIIllI('HOST')
IllIIIIIlIIIIllIIl = lllllllllllllll(lIlIllllIIIllI('PORT'))
IIlIIIlIlIllIIlllI = llIlllIIIIIllI(IllIIlIIllIlIl(IIIIlIllIIIlll(__file__), '..'))
IlllIlIIIIlIIIIllI = IllIIlIIllIlIl(IIlIIIlIlIllIIlllI, 'server', 'ssl', 'server.crt')
IlIIIllIIIIIIIllII = IllIIlIIllIlIl(IIlIIIlIlIllIIlllI, 'server', 'ssl', 'server.key')
IIllllllllllIllIII = lIlIllllIIIllI('DB_NAME')
lIlllllIllIlIIlIIl = lIlIllllIIIllI('DB_PASS')
IIlIIlIIlIIIlIIIII = lIlIllllIIIllI('DB_HOST')
IlIlIllIIIlllllIII = lIlIllllIIIllI('DB_USER')
llIlIIIllllIllIlIl = lIlIllllIIIllI('SERVER_IP')
llllllIlIlIlIIllIl = 'vuln_reports.txt'
lIIIlIlIllIIIIlllI = lIlIllllIIIllI('VIRTUAL_GPUS', '').split(',')