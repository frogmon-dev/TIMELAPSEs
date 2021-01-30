#!/bin/bash
cd /home/pi/TIMELAPs/bin/

find ./logs/*.log -ctime +30 -exec sudo rm -f {} \;
find ./pictures/*.jpg -ctime +100 -exec sudo rm -f {} \;
