#-*- coding:utf-8 -*-

# 중복 실행 방지
from tendo import singleton
try:
    me = singleton.SingleInstance()
except :
    print("another process running!")
    exit()

#프로그램 시작
import paho.mqtt.client as mqtt
import time
import json
from datetime import datetime
import requests
from picamera import PiCamera

from frogmon.uCommon  import COM
from frogmon.uGlobal  import GLOB
from frogmon.uRequest import REQUEST
from frogmon.uLogger  import LOG

#from frogmon.ulogger import LOG
configFileNM = COM.gHomeDir+COM.gSetupFile
controlFileNM = COM.gHomeDir+COM.gControlFile

mSvr_addr = GLOB.readConfig(configFileNM, 'MQTT', 'host_addr', 'frogmon.synology.me')
mSvr_port = GLOB.readConfig(configFileNM, 'MQTT', 'host_port', '8359')

user_id   = GLOB.readConfig(configFileNM, 'SETUP', 'user_id', '0')
dev_id    = GLOB.readConfig(configFileNM, 'SETUP', 'product_id', '0')

mSub_nm   = "FARMs/Control/%s/%s" % (user_id, dev_id)
mPub_nm   = "FARMs/Status/%s/%s" % (user_id, dev_id)

def callImgUploadAPI(fileName):
    url = 'https://frogmon.synology.me:5184/api/imgUpload'
    data = {
        'user_id': user_id,
        'product_id': dev_id
    }    
    with open(fileName, 'rb') as img_file:
        files = {'file': img_file}
        response = requests.post(url, data=data, files=files)
    print(response.text)


def captureOnce():
    size_x  = int(GLOB.readConfig(configFileNM, 'SETUP', 'resolution_x', '1920'))
    size_y  = int(GLOB.readConfig(configFileNM, 'SETUP', 'resolution_y', '1080'))
    mInterval  = int(GLOB.readConfig(configFileNM, 'SETUP', 'interval', '60'))
    mRotation  = int(GLOB.readConfig(configFileNM, 'SETUP', 'rotation', '0'))

    # pi camera Setting
    camera = PiCamera()
    camera.resolution = (size_x,size_y)
    camera.rotation = mRotation             #회전

    try:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S') 
        file_path = '/home/pi/TIMELAPSEs/images/image%s.jpg' % timestamp
        camera.capture(file_path)
        callImgUploadAPI(file_path)
    except Exception as e:
        print("error : %s" % e)
    finally:
        camera.close()
    

def getInfo():
    response_message = {}
    size_x  = int(GLOB.readConfig(configFileNM, 'SETUP', 'resolution_x', '1920'))
    size_y  = int(GLOB.readConfig(configFileNM, 'SETUP', 'resolution_y', '1080'))
    mInterval  = int(GLOB.readConfig(configFileNM, 'SETUP', 'interval', '60'))
    mRotation  = int(GLOB.readConfig(configFileNM, 'SETUP', 'rotation', '0'))
    
    response_message['width'] = size_x
    response_message['hight'] = size_y
    response_message['interval'] = mInterval
    response_message['rotation'] = mRotation
    response_message['button'] = 'click'
    response_message['image'] = 'still'
    return response_message
    

#서버로부터 CONNTACK 응답을 받을 때 호출되는 콜백
def on_connect(client, userdata, flags, rc):
    LOG.writeLn("[MQTT] Connected with result code "+str(rc))
    client.subscribe("%s" % mSub_nm) #구독 "nodemcu"

#서버로부터 publish message를 받을 때 호출되는 콜백
def on_message(client, userdata, msg):
    
    strJson = msg.payload.decode()
    LOG.writeLn("[MQTT] "+ msg.topic+" "+ strJson) #토픽과 메세지를 출력한다.
    try:
        status = GLOB.getJsonVal(strJson, 'status', 99)
        if (status != 0):
            response_message = getInfo()
            client.publish(mPub_nm, json.dumps(response_message))
        
        button = GLOB.getJsonVal(strJson, 'button', '0')
        if (button != '0'):
            print('get click')
            captureOnce()
            response_message = getInfo()
            client.publish(mPub_nm, json.dumps(response_message))
    except Exception as e :
        LOG.writeLn("[MQTT] : error : %s" % e)

print('')
print('--------------------------------------------------')
print('**  Welcome to FROGMON corp.')
print("**  Let's make it together")
print("**  ")
print('**  USER = %s' % user_id)
print('**  PRODUCT = %s' % dev_id)
print('**  CHNNEL_ID = %s' % mSub_nm)
print('--------------------------------------------------')
print('')

client = mqtt.Client() #client 오브젝트 생성
client.on_connect = on_connect #콜백설정
client.on_message = on_message #콜백설정

try:
    client.connect(mSvr_addr, int(mSvr_port), 60) #라즈베리파이3 MQTT 브로커에 연결
    client.loop_forever()
except Exception as e :
    LOG.writeLn("[MQTT] : error : %s" % e)
