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

mSub_nm   = "DIYs/%s/%s" % (user_id, dev_id)

#서버로부터 CONNTACK 응답을 받을 때 호출되는 콜백
def on_connect(client, userdata, flags, rc):
	LOG.writeLn("[MQTT] Connected with result code "+str(rc))
	client.subscribe("%s" % mSub_nm) #구독 "nodemcu"

#서버로부터 publish message를 받을 때 호출되는 콜백
def on_message(client, userdata, msg):
	strJson = msg.payload.decode()
	LOG.writeLn("[MQTT] "+ msg.topic+" "+ strJson) #토픽과 메세지를 출력한다.
	try:
		if GLOB.saveJsonData(COM.gJsonDir+"action.json", strJson) == 0:
			remote = '0'
			grp1 = GLOB.getJsonVal(strJson, 'interval', '0')
			if (grp1 != '0') :
				GLOB.writeConfig(configFileNM, 'SETUP', 'interval', grp1)
				remote = '1'
			grp2 = GLOB.getJsonVal(strJson, 'resolution_x', '0')
			if (grp2 != '0') :
				GLOB.writeConfig(configFileNM, 'SETUP', 'resolution_x', grp2)
				remote = '1'
			grp3 = GLOB.getJsonVal(strJson, 'resolution_y', '0')
			if (grp3 != '0') :
				GLOB.writeConfig(configFileNM, 'SETUP', 'resolution_y', grp3)
				remote = '1'
			grp4 = GLOB.getJsonVal(strJson, 'rotation', '99')
			if (grp4 != '99') :
				GLOB.writeConfig(configFileNM, 'SETUP', 'rotation', grp4)
				remote = '1'
			grp5 = GLOB.getJsonVal(strJson, 'start_time', '99')
			if (grp5 != '99') :
				GLOB.writeConfig(configFileNM, 'SETUP', 'start_time', grp5)
				remote = '1'
			grp6 = GLOB.getJsonVal(strJson, 'end_time', '99')
			if (grp6 != '99') :
				GLOB.writeConfig(configFileNM, 'SETUP', 'end_time', grp6)
				remote = '1'
			
			print('grps = %s %s %s %s %s %s [%s]' % (grp1, grp2, grp3, grp4, grp5, grp6, remote))
			
			if remote == '1' :
				if GLOB.appendTIMELAPsControlInfo(COM.gJsonDir+"device.json", GLOB.readConfig(configFileNM, 'SETUP', 'interval', '0')
				, GLOB.readConfig(configFileNM, 'SETUP', 'resolution_x', '0')
				, GLOB.readConfig(configFileNM, 'SETUP', 'resolution_y', '0')
				, GLOB.readConfig(configFileNM, 'SETUP', 'rotation', '0')
				, GLOB.readConfig(configFileNM, 'SETUP', 'start_time', '0')
				, GLOB.readConfig(configFileNM, 'SETUP', 'end_time', '0')
				) == 0 :
					REQUEST.updateDIYs(user_id, dev_id)
					LOG.writeLn("[MQTT] Command recive and reboot in 3 sec")
					time.sleep(3)
					run_command("sudo reboot")
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
