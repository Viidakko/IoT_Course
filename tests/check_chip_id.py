#-------------------
# Chip ID Verification Script
# Reads and prints the chip ID from a BMP280/BME280 sensor at address 0x76.
# Used to verify the sensor is correctly connected and responding.
# Expected values: 0x58 (BMP280) or 0x60 (BME280).
#-------------------

import machine
from machine import Pin

i2c = machine.I2C(id=1, sda=Pin(2), scl=Pin(3))
print(hex(i2c.readfrom_mem(0x76, 0xD0, 1)[0]))