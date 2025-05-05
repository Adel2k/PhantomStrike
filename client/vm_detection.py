import sys
import os
import subprocess
import platform

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


VIRTUAL_GPUS = [
	"vmware", "hyper-v", "parallels", "qemu", "virtualbox",
	"virtio", "cirrus", "microsoft basic display adapter"
]

def get_os() -> str:
	return platform.system().lower()

def get_gpu_info() -> str:
	os_name = get_os()

	try:
		if os_name == "linux":
			output = subprocess.check_output("lspci | grep -i vga",
												shell=True).decode().lower()
		elif os_name == "windows":
			output = subprocess.check_output("wmic path win32_videocontroller get name",
												shell=True).decode().lower()
		elif os_name == "darwin":
			output = subprocess.check_output("system_profiler SPDisplaysDataType",
												shell=True).decode().lower()
		else:
			return "unknown"
		return output.strip()

	except Exception as e:
		return "error"

def is_vm() -> bool:
	gpu_info = get_gpu_info()
	return any(virtual_gpu in gpu_info for virtual_gpu in VIRTUAL_GPUS)
