#!/bin/bash

CRON_JOB="@reboot $(which nohup) $(which python3) $(find / -name is_running.py) >> /home/$(echo $USER)/cron.log 2>&1 &"

crontab -l | grep -F "$CRON_JOB" > /dev/null
if [ $? -eq 0 ]; then
    echo "Cron job already exists."
else
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "Cron job added."
fi
