import os
import time
import sys
def is_running():
    try:
        result = os.popen("pgrep -f client.py").read()
        if result.strip():
            print("client.py is already running.")
            return True
        else:
            print("client.py is not running.")
            return False
    except Exception as e:
        print(f"Error checking process: {e}")
        return False
while True:
    try:
        if not is_running():
            print("Starting client.py...")
            os.system("nohup python3 /home/potato/Desktop/PhantomStrike/client/client.py &")
        time.sleep(60)
    except Exception as e:
        print(f"Error in main loop: {e}")
