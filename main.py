from machine import Pin, I2C
import network
import time
from bme import BME280
from umqtt.simple import MQTTClient
import ssl
import config

led_pin = Pin('LED', Pin.OUT)

# Setup Wi-Fi
ssid = config.ssid
password = config.pwd

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

connection_timeout = 10
while connection_timeout > 0:
    if wlan.status() == 3:  # Connected
        break
    connection_timeout -= 1
    print('Waiting for Wi-Fi connection...')
    time.sleep(1)

# Check if connection was successful
if wlan.status() != 3:
    led_pin.on()
    time.sleep_ms(1000)
    led_pin.off()
    raise RuntimeError('[ERROR] Failed to establish a network connection')
else:
    led_pin.on()
    time.sleep_ms(500)
    led_pin.off()
    time.sleep_ms(500)
    led_pin.on()
    time.sleep_ms(500)
    led_pin.off()
    print('[INFO] CONNECTED!')
    network_info = wlan.ifconfig()
    print('[INFO] IP address:', network_info[0])

# Config SSL connection with Transport Layer Security encryption (no cert)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)  # Connect as client, not server/broker
context.verify_mode = ssl.CERT_NONE  # Do not verify server/broker cert

# MQTT client connect
client = MQTTClient(
    client_id=b'tumi_picow',
    server=config.MQTT_BROKER,
    port=config.MQTT_PORT,
    user=config.MQTT_USER,
    password=config.MQTT_PWD,
    ssl=context
)
client.connect()

# Define I2C connection and BMP
#i2c = I2C(id=0, sda=Pin(20), scl=Pin(21))  # id=channel
#bme = BME280(i2c=i2c)

# Publish function
def publish(mqtt_client, topic, value):
    mqtt_client.publish(topic, value)
    print("[INFO][PUB] Published {} to {} topic".format(value, topic))

# Unified callback function
def on_message(topic, msg):
    topic = topic.decode()
    print(f"Received message: {msg} on topic: {topic}")
    
    if topic == "picow/control":
        if msg == b"ON":
            led_pin.on()  # Turn on the temperature pin
            print("Optimal temperature reached")
        elif msg == b"OFF":
            led_pin.on()
            time.sleep_ms(500)
            led_pin.off()
            time.sleep_ms(500)
            led_pin.on()
            time.sleep_ms(500)
            led_pin.off()
            time.sleep_ms(500)
            led_pin.on()
            time.sleep_ms(500)
            led_pin.off()
            print("Heating Apartment")
    

client.set_callback(on_message)
client.subscribe(b"picow/control")


# Main loop
while True:
    # Publish MQTT payload
    client.check_msg()

    # Every 2s
    time.sleep_ms(1000)


