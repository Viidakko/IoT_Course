import machine
from machine import Pin

i2c = machine.I2C(id=1, sda=Pin(2), scl=Pin(3))
print(hex(i2c.readfrom_mem(0x76, 0xD0, 1)[0]))