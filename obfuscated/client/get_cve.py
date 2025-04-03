lllllllllllllll, llllllllllllllI, lllllllllllllIl = str, len, list
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from imports.config import *

def IIIllllllIllIIllll(IlIllllIllIlIIIlll):
    IllIIllIlllIlllIlI = 0
    while IllIIllIlllIlllIlI < llllllllllllllI(IlIllllIllIlIIIlll):
        if IlIllllIllIlIIIlll[IllIIllIlllIlllIlI:IllIIllIlllIlllIlI + 4] == 'CVE-':
            IllIIIIIllllIIIlll = ''
            while IllIIllIlllIlllIlI < llllllllllllllI(IlIllllIllIlIIIlll) and IlIllllIllIlIIIlll[IllIIllIlllIlllIlI] != ' ' and (IlIllllIllIlIIIlll[IllIIllIlllIlllIlI] != ','):
                IllIIIIIllllIIIlll += IlIllllIllIlIIIlll[IllIIllIlllIlllIlI]
                IllIIllIlllIlllIlI += 1
            return IllIIIIIllllIIIlll
        IllIIllIlllIlllIlI += 1
    return ''

def llIlllIIlIllIlIIII(lllllIlIllIlIIIlII):
    IIIIlIIIlIIllIlIll = []
    lIlllIIlIIIIIllllI = nmap.PortScanner()
    IlIlIIlIIllIIlIIll = lIlllIIlIIIIIllllI.scan(hosts=lllllIlIllIlIIIlII, arguments='-p21,25,80 --script vuln')
    for IIIIIIlIllIlllllII in IlIlIIlIIllIIlIIll['scan']:
        for llllIllIIlIIlIlllI in IlIlIIlIIllIIlIIll['scan'][IIIIIIlIllIlllllII]:
            if llllIllIIlIIlIlllI in ['tcp', 'udp']:
                for (lIlIIllIIIIlIlIIII, llIIIllIIIlIIIlIIl) in IlIlIIlIIllIIlIIll['scan'][IIIIIIlIllIlllllII][llllIllIIlIIlIlllI].items():
                    llllIllIllIllllllI = llIIIllIIIlIIIlIIl.get('name', '')
                    llIIIIIlIIIllIIlll = []
                    if 'script' in llIIIllIIIlIIIlIIl:
                        for lIIIIlIlIIIIIIIIII in llIIIllIIIlIIIlIIl['script'].values():
                            llIIIIIlIIIllIIlll.extend([lIlIlllIlIlIIIIIII for lIlIlllIlIlIIIIIII in lIIIIlIlIIIIIIIIII.split('\n') if 'CVE-' in lIlIlllIlIlIIIIIII])
                    if llIIIIIlIIIllIIlll:
                        llIlIllllIIIIIIllI = ', '.join(llIIIIIlIIIllIIlll)
                        IIIIlIIIlIIllIlIll.append({'port': lIlIIllIIIIlIlIIII, 'service': llllIllIllIllllllI, 'cve': IIIllllllIllIIllll(llIlIllllIIIIIIllI)})
    return IIIIlIIIlIIllIlIll