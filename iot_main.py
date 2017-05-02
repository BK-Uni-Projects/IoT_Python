## IoT Assignment
from mcp3008 import *							# using spidev to read the MPC3008 ADC 
from time import sleep							# for pausing execution
from AzureConnect import *						# Functions and settings for connecting to azure web service
import RPi.GPIO as GPIO							# GPIO library Used fo LED outputs

## IoT Assignment - creating a unique hashcode
import hashlib									# For hashing the time
import time 									# for something to hash


# Setup data types for program
OFF, ON = range(2)								# Logical Enums for LEDs etc

# LED GPIO Pins
Temp_HIGH = 21		# red
Temp_MED = 20		# yellow
Temp_LOW = 16		# green

Soil_01_LOW = 26	# red
Soil_01_OK = 19		# green

Soil_02_LOW = 06	# red
Soil_02_OK = 05		# green

#	Setup Sensor IDs (3008 input channels)
Temperature_1 	= 0
Temperature_2 	= 1
SoilSensor_1 	= 2

def CreateHashCode(size):
	#hashcode = hash.hexdigest()[:20]
	hash = hashlib.sha1()
	hash.update(str(time.time()))
	return hash.hexdigest()[:size]

def InitialiseGPIO():
	GPIO.setmode(GPIO.BCM)						# Set GPIO to use BCM Pinout mode
	GPIO.setwarnings(False)						# Disable warnings
	
	GPIO.setup(21,GPIO.OUT)
	GPIO.setup(20,GPIO.OUT)
	GPIO.setup(16,GPIO.OUT)
	
	GPIO.setup(26,GPIO.OUT)
	GPIO.setup(19,GPIO.OUT)
	
	GPIO.setup(06,GPIO.OUT)
	GPIO.setup(05,GPIO.OUT)

def CleanupGPIO():
	## Switch OFF all LEDs
	GPIO.output(Temp_HIGH, GPIO.LOW)
	GPIO.output(Temp_MED, GPIO.LOW)
	GPIO.output(Temp_LOW, GPIO.LOW)
	
	GPIO.output(Soil_01_LOW, GPIO.LOW)
	GPIO.output(Soil_01_OK, GPIO.LOW)
	
	GPIO.output(Soil_02_LOW, GPIO.LOW)
	GPIO.output(Soil_02_OK, GPIO.LOW)
	
def TestGPIO():
	## Switch on All LEDs
	GPIO.output(Temp_HIGH, GPIO.HIGH)
	GPIO.output(Temp_MED, GPIO.HIGH)
	GPIO.output(Temp_LOW, GPIO.HIGH)
	
	GPIO.output(Soil_01_LOW, GPIO.HIGH)
	GPIO.output(Soil_01_OK, GPIO.HIGH)
	
	GPIO.output(Soil_02_LOW, GPIO.HIGH)
	GPIO.output(Soil_02_OK, GPIO.HIGH)
	
	## Wait 5 seconds
	time.sleep(5)

	## Switch OFF all LEDs
	GPIO.output(Temp_HIGH, GPIO.LOW)
	GPIO.output(Temp_MED, GPIO.LOW)
	GPIO.output(Temp_LOW, GPIO.LOW)
	
	GPIO.output(Soil_01_LOW, GPIO.LOW)
	GPIO.output(Soil_01_OK, GPIO.LOW)
	
	GPIO.output(Soil_02_LOW, GPIO.LOW)
	GPIO.output(Soil_02_OK, GPIO.LOW)
		
def readAnalog(channel):
	print ("Channel {0}: {1}".format(channel, getReading(channel)))
	print ("Channel {0}: {1}".format(channel, ReadChannel(channel)))
	print
		
def ReadSoil(channel): 	
	humid = round(getReading(channel), 2)
	humid = humid / 1000 * 100
	return humid
  
def UpdateDatabase(PostSensor, PostType, PostVal):
	RespPost = requests.post(MainURL + PostURL, params=AddData(PostSensor, PostType, PostVal))
	
def sensortest():
	for x in range(0,5):
		print
		for x in range(0,3):
			readAnalog(x)
			
		print ReadSoil(SoilSensor_1)
		print ConvertTemp(getReading(Temperature_1), 2)
		
		print("Soil Dryness at {0}%".format(ReadSoil(SoilSensor_1)))
		print("Temperature 1 at {0}C".format(ConvertTemp(getReading(Temperature_1), 2)))
		
		sleep(2)
		
def sampleTemp(sensor):
	temp = ConvertTemp(getReading(Temperature_1), 2)
	flag = 0
	if temp > 40:
		flag=1
		GPIO.output(Temp_HIGH, GPIO.HIGH)
		GPIO.output(Temp_MED, GPIO.LOW)
		GPIO.output(Temp_LOW, GPIO.LOW)	
	
	if temp < 20:
		flag=1
		GPIO.output(Temp_HIGH, GPIO.LOW)
		GPIO.output(Temp_MED, GPIO.LOW)
		GPIO.output(Temp_LOW, GPIO.HIGH)
		
	if flag == 0:
		flag=1	
		GPIO.output(Temp_HIGH, GPIO.LOW)
		GPIO.output(Temp_MED, GPIO.LOW)
		GPIO.output(Temp_LOW, GPIO.HIGH)
		
	if debug == 1:
		print ConvertTemp(getReading(Temperature_1), 2)		
		
	## TODO	
	# Send data to server
	PostSensor = 0				# Default value to stop errors
	if sensor == 0:
		PostSensor = 6
		
	if sensor == 1:
		PostSensor = 7
	
	PostType = 'Temperature'
	PostVal = temp
	
	#print("post = {0}{1}".format(MainURL + PostURL, AddData(PostSensor, PostType, PostVal)))
	#, params=AddData(PostSensor, PostType, PostVal)))
	
	UpdateDatabase(PostSensor, PostType, PostVal)
	#print("RespPost = {0}".format(RespPost))
	
	
# Program Start
debug = 1

InitialiseGPIO()

for x in range(0, 60):
	sampleTemp(Temperature_1)
	sleep(1)

returnedData = getSensorData(6)
print json.dumps(returnedData.json())


## Program Complete	tidy up
CleanupGPIO()


















