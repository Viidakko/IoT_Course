import machine
from machine import Pin
from bmp280 import BME280
import time

i2c = machine.I2C(id=1, sda=Pin(2), scl=Pin(3))
bmp = BME280(i2c=i2c)

while True:
    print("Temp: ", bmp.temperature, "Pressure: ", bmp.pressure)
    time.sleep_ms(1000)