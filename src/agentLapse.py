from picamera import PiCamera
from time import sleep
from datetime import datetime
import subprocess
import requests

from frogmon.uCommon    import COM
from frogmon.uConfig    import CONF

config = CONF(COM.gHomeDir+COM.gSetupFile)

user_id = config.readConfig('SETUP', 'user_id', '')
dev_id  = config.readConfig('SETUP', 'product_id', '')
size_x  = config.readConfig('SETUP', 'resolution_x', '1920')
size_y  = config.readConfig('SETUP', 'resolution_y', '1080')
mInterval  = config.readConfig('SETUP', 'interval', '60')
mRotation  = config.readConfig('SETUP', 'rotation', '0')


def callImgUploadAPI(fileName):
    url = 'https://frogmon.synology.me:5184/api/imgUpload'
    data = {
        'user_id': user_id,
        'product_id': dev_id
    }    
    with open(file_path, 'rb') as img_file:
        files = {'file': img_file}
        response = requests.post(url, data=data, files=files)
    print(response.text)

# pi camera Setting
camera = PiCamera()
camera.resolution = (size_x,size_y)
camera.rotation = mRotation             #회전

#camera.start_preview()
while True:
    try:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S') 
        file_path = '/home/pi/TIMELAPSEs/images/image%s.jpg' % timestamp
        camera.capture(file_path)
        subprocess.run(["/home/pi/TIMELAPSEs/src/imageUpdate.sh", file_path], check=True)
        callImgUploadAPI(file_path)
    except Exception as e:
        print("error : %s" % e)
    sleep(mInterval)
    	
        
#camera.stop_preview()
