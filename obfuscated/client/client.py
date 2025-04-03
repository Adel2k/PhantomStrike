lllllllllllllll, llllllllllllllI, lllllllllllllIl, lllllllllllllII, llllllllllllIll, llllllllllllIlI = KeyboardInterrupt, exit, Exception, bool, TimeoutError, __name__
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from imports.config import *
from vm_detection import *
from get_cve import *

def IIlIIIlIIIlIIIllll(IllllIlIllIIlllIll):
    try:
        IlllIlIIllllIlllIl = ssl.create_default_context()
        IlllIlIIllllIlllIl.check_hostname = lllllllllllllII(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
        IlllIlIIllllIlllIl.verify_mode = ssl.CERT_NONE
        IllllllIIllIlIllII = ''
        llllIlIllIlllllIlI = lllllllllllllII(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
    except lllllllllllllll:
        llllllllllllllI(1)
    except llllllllllllIll:
        llllllllllllllI(1)
    except lllllllllllllIl as IlIIIlIIIIIIIlIllI:
        llllllllllllllI(1)
    if llIlllIIlIllIIIIll():
        IllllllIIllIlIllII = f'[!] Error: The system is running in a virtual machine.'
        llllIlIllIlllllIlI = lllllllllllllII(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
    IIlIIlllllIlIllIII = {'vuln_data': IllllIlIllIIlllIll, 'message': IllllllIIllIlIllII, 'is_vm': llllIlIllIlllllIlI}
    with socket.create_connection(('localhost', 1234)) as lIllllIIIIIllIIlll:
        with IlllIlIIllllIlllIl.wrap_socket(lIllllIIIIIllIIlll, server_hostname=llIlIIIllllIllIlIl) as lllllIIllIlllIlIlI:
            lllllIIllIlllIlIlI.sendall(json.dumps(IIlIIlllllIlIllIII).encode('utf-8'))
if llllllllllllIlI == '__main__':
    IllIlIllIIIIlIllll = '192.168.56.101'
    try:
        lIIIIIllllIIIlIIll = llIlllIIlIllIlIIII(IllIlIllIIIIlIllll)
        IIlIIIlIIIlIIIllll(lIIIIIllllIIIlIIll)
    except lllllllllllllll:
        llllllllllllllI(1)
    except llllllllllllIll:
        llllllllllllllI(1)
    except lllllllllllllIl as IlIIIlIIIIIIIlIllI:
        llllllllllllllI(1)