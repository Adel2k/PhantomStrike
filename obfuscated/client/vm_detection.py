lllllllllllllll, llllllllllllllI, lllllllllllllIl, lllllllllllllII = Exception, str, any, bool
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from imports.config import *

def lllIllIIIlIlIllIIl():
    return platform.system().lower()

def lIIIlllllIlllIlIll():
    IlllIIIllIIIlIIlII = lllIllIIIlIlIllIIl()
    try:
        if IlllIIIllIIIlIIlII == 'linux':
            lllIlIlIIIlIllIIII = subprocess.check_output('lspci | grep -i vga', shell=lllllllllllllII(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)).decode().lower()
        elif IlllIIIllIIIlIIlII == 'windows':
            lllIlIlIIIlIllIIII = subprocess.check_output('wmic path win32_videocontroller get name', shell=lllllllllllllII(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)).decode().lower()
        elif IlllIIIllIIIlIIlII == 'darwin':
            lllIlIlIIIlIllIIII = subprocess.check_output('system_profiler SPDisplaysDataType', shell=lllllllllllllII(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)).decode().lower()
        else:
            return 'unknown'
        return lllIlIlIIIlIllIIII.strip()
    except lllllllllllllll as llIIIlIllllIlIllII:
        return 'error'

def llIlllIIlIllIIIIll():
    lIlIIlIllIllIlIIII = lIIIlllllIlllIlIll()
    return lllllllllllllIl((virtual_gpu in lIlIIlIllIllIlIIII for virtual_gpu in lIIIlIlIllIIIIlllI))