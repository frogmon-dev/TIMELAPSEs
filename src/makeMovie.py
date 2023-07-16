import cv2
import os
from datetime import datetime
import subprocess

image_folder = '../images'  # 이미지 파일들이 있는 폴더

theDate = datetime.now().strftime('%Y%m%d') 
video_name = '../video/%s.avi' % theDate  # 생성할 비디오 파일의 이름

images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]

# 파일 이름에서 날짜와 시간을 추출하여 이를 기반으로 정렬합니다.
# 'image년월일시분초.jpg' 형식을 가정합니다.
images.sort(key=lambda x: datetime.strptime(x.split('image')[1].split('.jpg')[0], '%Y%m%d%H%M%S'))

frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'DIVX'), 30, (width, height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

subprocess.run(["/home/pi/TIMELAPSEs/src/fileUploader.sh", video_name], check=True)

cv2.destroyAllWindows()
video.release()