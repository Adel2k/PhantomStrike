import nmap

def get_cve_from_line(s: str) -> str:
	i = 0;
	while i < len(s):
		if s[i:i+4] == "CVE-":
			cve = ""
			while i < len(s) and s[i] != " " and s[i] != ",":
				cve += s[i]
				i += 1
			return cve
		i += 1
	return ""

def run_scan() -> list:
	cves = []
	scanner = nmap.PortScanner()
	result = scanner.scan(hosts='192.168.123.50', arguments='-sS -sU -p 20-100 --script vuln')

	for host in result['scan']:
		for proto in result['scan'][host]:
			if proto in ['tcp', 'udp']:
				for port, port_info in result['scan'][host][proto].items():
					service = port_info['name']
					cve_list = []

					if 'script' in port_info:
						for script_output in port_info['script'].values():
							cve_list.extend([line for line in script_output.split("\n") if "CVE-" in line])

					if cve_list:
						cve_str = ", ".join(cve_list)
						cves.append({"port": port, "service": service, "cve": get_cve_from_line(cve_str)})
	return cves

print(run_scan())