#!/usr/bin/python

# from http://www.raspberrypi-spy.co.uk/2013/10/analogue-sensors-on-the-raspberry-pi-using-an-mcp3008/

import spidev
import time
import os

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
 
def getReading(channel):
	rawData = spi.xfer([1, (8 + channel) << 4, 0])
	processData = ((rawData[1]&3) <<8)+rawData[2]
	return processData

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
	adc = spi.xfer2([1,(8+channel)<<4,0])
	data = ((adc[1]&3) << 8) + adc[2]
	return data

def ReadInput(Sensor):
    adc = spi.xfer2([1,(8+Sensor)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data


# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def ConvertVolts(data,places):
  volts = (data * 3.3) / float(1023)
  volts = round(volts,places)
  return volts
 
# Function to calculate temperature from
# TMP36 data, rounded to specified
# number of decimal places.
def ConvertTemp(data,places):
 
  # ADC Value
  # (approx)  Temp  Volts
  #    0      -50    0.00
  #   78      -25    0.25
  #  155        0    0.50
  #  233       25    0.75
  #  310       50    1.00
  #  465      100    1.50
  #  775      200    2.50
  # 1023      280    3.30
 
  temp = ((data * 330)/float(1023))-50
  temp = round(temp,places)
  return temp
 
# Define sensor channels
light_channel = 0
temp_channel  = 1
 
# Define delay between readings
delay = 5
'''
# Read the light sensor data
light_level = ReadChannel(light_channel)
light_volts = ConvertVolts(light_level,2)

# Read the temperature sensor data
temp_level = ReadChannel(temp_channel)
temp_volts = ConvertVolts(temp_level,2)
temp       = ConvertTemp(temp_level,2)

# Print out results
print "--------------------------------------------"
print("Light: {} ({}V)".format(light_level,light_volts))
print("Temp : {} ({}V) {} deg C".format(temp_level,temp_volts,temp))
  
while True: 
  # Wait before repeating loop
  time.sleep(delay)
'''
 