#!/bin/bash

OS="$(uname -s)"

if [[ "$OS" == "Linux" ]]; then
    echo "[*] Detected Linux."

    CRON_JOB="@reboot /usr/bin/nohup /usr/bin/python3 $PWD/client.py >> /home/potato/cron.log 2>&1 &"

    crontab -l 2>/dev/null | grep -F "$CRON_JOB" > /dev/null
    if [ $? -eq 0 ]; then
        echo "Cron job already exists."
    else
        (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
        echo "Cron job added."
    fi

elif [[ "$OS" == *"MINGW"* || "$OS" == *"CYGWIN"* || "$OS" == *"MSYS"* ]]; then
    echo "[*] Detected Windows."

    powershell.exe -ExecutionPolicy Bypass -File ./windows_startup_script.ps1

else
    echo "Unsupported OS: $OS"
fi
