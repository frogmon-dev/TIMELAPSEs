#!/bin/bash

python3 /home/pi/TIMELAPs/src/timeLapse.py &

python3 /home/pi/TIMELAPs/src/timeMqtt.py &

exit