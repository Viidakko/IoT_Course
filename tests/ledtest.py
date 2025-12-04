#-------------------
# LED Blink Test Script
# Simple test script to blink the onboard LED of the Pico W.
# Toggles the LED on/off every 500ms in an infinite loop.
#-------------------

from machine import Pin
import time

led = Pin("LED", Pin.OUT)

while True:
    led.on()
    time.sleep_ms(500)
    led.off()
    time.sleep_ms(500)