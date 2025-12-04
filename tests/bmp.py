#-------------------
# BMP280 Sensor Test Script
# Reads temperature and pressure data from a BMP280/BME280 sensor
# via I2C and prints readings every second to the console.
# Requires bmp280.py driver file from src folder.
#-------------------

import sys
sys.path.insert(0, '../src')

import machine
from machine import Pin
from bmp280 import BME280
import time

i2c = machine.I2C(id=1, sda=Pin(2), scl=Pin(3))
bmp = BME280(i2c=i2c)

while True:
    print("Temp: ", bmp.temperature, "Pressure: ", bmp.pressure)
    time.sleep_ms(1000)