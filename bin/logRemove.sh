#!/bin/bash
find ./logs/*.log -ctime +30 -exec sudo rm -f {} \;
find ./pictures/*.jpg -ctime +100 -exec sudo rm -f {} \;
