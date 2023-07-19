from picamera import PiCamera
from time import sleep
from datetime import datetime
import requests
import subprocess

from frogmon.uCommon    import COM
from frogmon.uConfig    import CONF
from frogmon.uGlobal  	import GLOB

configFileNM = COM.gHomeDir+COM.gSetupFile

user_id = GLOB.readConfig(configFileNM, 'SETUP', 'user_id', '')
dev_id  = GLOB.readConfig(configFileNM, 'SETUP', 'product_id', '')
size_x  = int(GLOB.readConfig(configFileNM, 'SETUP', 'resolution_x', '1920'))
size_y  = int(GLOB.readConfig(configFileNM, 'SETUP', 'resolution_y', '1080'))
mInterval  = int(GLOB.readConfig(configFileNM, 'SETUP', 'interval', '60'))
mRotation  = int(GLOB.readConfig(configFileNM, 'SETUP', 'rotation', '0'))
mStartTime = int(GLOB.readConfig(configFileNM, 'SETUP', 'start_time', '0'))
mEndTime   = int(GLOB.readConfig(configFileNM, 'SETUP', 'end_time', '24'))

def captureOnce():
    # pi camera Setting
    camera = PiCamera()
    camera.resolution = (size_x,size_y)
    camera.rotation = mRotation             #회전

    try:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')         
        file_path = '/home/pi/TIMELAPSEs/images/image%s.jpg' % timestamp
        camera.capture(file_path)
        #subprocess.run(["/home/pi/TIMELAPSEs/src/imageUpdate.sh", file_path], check=True)        
        callImgUploadAPI(file_path)
    except Exception as e:
        print("error : %s" % e)
    

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

current_hour = int(datetime.now().strftime("%H"))
if(mStartTime<=current_hour and current_hour<= mEndTime):
    captureOnce()    	
        
#camera.stop_preview()
