import os
import time
import sys

def is_running():
    """Checks if the script is running by checking process IDs."""
    try:
        result = os.popen("ps aux | grep client.py | grep -v grep").read()
        if result:
            return True
        return False
    except Exception as e:
        return False

while True:
    if not is_running():
        os.system("python3 /home/potato/Desktop/PhantomStrike/client/client.py &")
    time.sleep(60)
