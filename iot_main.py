## IoT Workshops
from twython import Twython, TwythonError		# Twython is used for getting and recieving twitter data
from TwitterIdentity import twitter				# Personal data hidden by a separate file
from HIH6130.io import HIH6130					# Sparkfun temperature and humidity sensor
from bmp180 import *							# BMP180 Barometer sensor

## IoT Assignment
from mcp3008 import *							# using spidev to read the MPC3008 ADC 
from time import sleep							# for pausing execution
from AzureConnect import *						# Functions and settings for connecting to azure web service
import RPi.GPIO as GPIO							# GPIO library Used fo LED outputs

## IoT Assignment - creating a unique hashcode
import hashlib									# For hashing the time
import time 									# for something to hash

ON, OFF = range(2)


def CreateHashCode():
	hash = hashlib.sha1()
	hash.update(str(time.time()))
	return hash


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

	
def TestGPIO():
	## Switch on All LEDs
	GPIO.output(21,GPIO.HIGH)
	GPIO.output(20,GPIO.HIGH)
	GPIO.output(16,GPIO.HIGH)
	
	GPIO.output(26,GPIO.HIGH)
	GPIO.output(19,GPIO.HIGH)
	
	GPIO.output(06,GPIO.HIGH)
	GPIO.output(05,GPIO.HIGH)
	
	## Wait 5 seconds
	time.sleep(5)

	## Switch OFF all LEDs
	GPIO.output(21,GPIO.LOW)
	GPIO.output(20,GPIO.LOW)
	GPIO.output(16,GPIO.LOW)
	
	GPIO.output(26,GPIO.LOW)
	GPIO.output(19,GPIO.LOW)
	
	GPIO.output(06,GPIO.LOW)
	GPIO.output(05,GPIO.LOW)


#temperature/humidity sensor
def readhih6130():
	rht = HIH6130()
	rht.read()
	if debug == 1:
		print("Timestamp   : {0}".format(hash.hexdigest()[:20]))	# time
		print("Humidity    : {0}".format(rht.rh)) 			# humidity in %
		print("Temperature : {0}".format(rht.t))			# temp in C
		print

		
#read BMP180 sensor
def read180():
	(chip_id, chip_version) = readBmp180Id()
	(temperature,pressure) = readBmp180()
	if debug == 1:
		print("Temperature : {0}".format(temperature))		# temp in C
		print("Pressure    : {0}".format(pressure)) 		# pressure in mbar
		print 

		
def readAnalog():
	for x in range(0,8):
		print ("Channel {0}: {1}".format(x, getReading(x)))

		
def ReadSoilHumidity(channel): 	
	humid = round(getReading(channel), 2)
	return humid
  

	

# Program Start
debug = 0

InitialiseGPIO()
if debug == 1:
	TestGPIO()

# Setup Sensor IDs (3008 input channels)
SoilSensor1 = 2
Temperatur1 = 0

for x in range(0,5):
	print
	print(ON)
	print(OFF)
	readAnalog()
	print ReadSoilHumidity(2)/1000*100
	#print("Soil Dryness at {0}%".format(ReadSoilHumidity(SoilSensor1)))
	sleep(2)

#hashcode = hash.hexdigest()[:20]

#print hashcode

#print

#PostSensor = 3
#PostType = 'humidity'
#PostVal = 30	#rht.rh

#RespPost = requests.post(MainURL + PostURL, params=AddData(PostSensor, PostType, PostVal))

#RespGet = requests.get(MainURL+GetURL, params=mysensor(PostSensor))

#print json.dumps(RespGet.json())