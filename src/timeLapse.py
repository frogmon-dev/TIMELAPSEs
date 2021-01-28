# -*- coding: utf-8 -*- 

# 중복 실행 방지
from tendo import singleton
try:
    me = singleton.SingleInstance()
except :
    print("another process running!")
    exit()

import RPi.GPIO as GPIO
import time
import os
import random
from picamera import PiCamera

import json
import base64

from frogmon.uCommon  import COM
from frogmon.uGlobal  import GLOB
from frogmon.uRequest import REQUEST
from frogmon.uLogger  import LOG

# Functions
def makeJson():
    data = {}
    data['DEV_ID'] = mProduct_id
    data['VERSION'] = mVersion
    data['INTERVAL']     = mInterval_sec
    data['RES_X']        = mResolution_x
    data['RES_Y']        = mResolution_y
    data['ROTATION']     = mRotation
    data['START_TIME']   = mStart_time
    data['END_TIME']     = mEnd_time

    LOG.writeLn('json file save:%s' % COM.gJsonDir+'device.json')
    with open(COM.gJsonDir+'device.json', 'w', encoding='utf-8') as make_file:
        json.dump(data, make_file, indent="\t")	


# init
configFileNM = COM.gHomeDir+COM.gSetupFile
mUser_id        = GLOB.readConfig(configFileNM, 'SETUP', 'user_id', 'empty')
mProduct_id     = GLOB.readConfig(configFileNM, 'SETUP', 'product_id', 'empty')
mVersion        = GLOB.readConfig(configFileNM, 'SETUP', 'version', 'ver 1.0')
mInterval_sec   = int(GLOB.readConfig(configFileNM, 'SETUP', 'interval', '600'))
mResolution_x   = int(GLOB.readConfig(configFileNM, 'SETUP', 'resolution_x', '640'))
mResolution_y   = int(GLOB.readConfig(configFileNM, 'SETUP', 'resolution_y', '480'))
mRotation       = int(GLOB.readConfig(configFileNM, 'SETUP', 'rotation', '0'))
mStart_time     = int(GLOB.readConfig(configFileNM, 'SETUP', 'start_time', '0'))
mEnd_time       = int(GLOB.readConfig(configFileNM, 'SETUP', 'end_time', '23'))

GLOB.setUpdateTime()
makeJson()

print('')
print('--------------------------------------------------')
print('**  Welcome to FROGMON corp.')
print("**  Let's make it together")
print("**  ")
print('**  USER = %s'       % mUser_id)
print('**  PRODUCT = %s'    % mProduct_id)
print('**  NOW times = %s'  % COM.gstrYMDHMS)
print('**  INTERVAL = %s'   % mInterval_sec)
print('**  RES_X = %s'      % mResolution_x)
print('**  RES_Y = %s'      % mResolution_y)
print('**  ROTATION = %s'   % mRotation)
print('**  START_TIME = %s' % mStart_time)
print('**  END_TIME = %s'   % mEnd_time)
print('--------------------------------------------------')
print('')

# pi camera Setting
camera = PiCamera()
camera.resolution = (mResolution_x,mResolution_y)
camera.rotation = mRotation
counter = 1
decCnt = 0
updateInt = 0

LOG.writeLn("[timeLapse] process run")
# Main Process
while True:
    try:
        GLOB.setUpdateTime()
        GLOB.appendTIMELAPsControlInfo(COM.gJsonDir+"device.json", mInterval_sec, mResolution_x, mResolution_y, mRotation, mStart_time, mEnd_time)
        REQUEST.updateDIYs(mUser_id, mProduct_id)
        if (int(COM.gHH) >= mStart_time) and (int(COM.gHH) <= mEnd_time): 
            camera.start_preview()
            imgFileNm = COM.gHomeDir + 'pictures/pic_%s.jpg' % COM.gstrYMDHMS
            # make picture
            camera.capture(imgFileNm)
            camera.stop_preview()
            LOG.writeLn('file save:%s' % imgFileNm)
        time.sleep(mInterval_sec)
    except Exception as e :
        LOG.writeLn("[timeLapse] Error : %s" % e)
    
