import requests
import json

def mysensor(sensor):
	senseid = {"sensorid": sensor}
	return senseid
	
def AddData(id, type, value):
	payload = {"sensorid":id, "sensortype":type, "value":value}
	return payload

def getSensorData(reqsensor):
	RespGet = requests.get(MainURL+GetURL, params=mysensor(reqsensor))
	return RespGet

MainURL='http://bksiotworkshop.azurewebsites.net/index.php'
PostURL='/sensors/postsensordata'
GetURL='/sensors/getsensordata'

def UploadData(sensorid, sensortype, sensorvalue):
	RespPost - requests.post(MainURL+PostURL, params=AddData(sensorid, sensortype, sensorvalue))
	




