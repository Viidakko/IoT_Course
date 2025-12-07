#-------------------
# Main IoT Application
# Serves weather station page over HTTP.
# Handles logout to return to AP mode.
#-------------------

from machine import Pin, I2C, reset
import network
import socket
import time
import json
import os
import config
import html
from bmp280 import BME280

led_pin = Pin('LED', Pin.OUT)
CREDENTIALS_FILE = 'credentials.json'

# Get connection info
wlan = network.WLAN(network.STA_IF)
ip_address = wlan.ifconfig()[0]

# Load saved network info
try:
    with open(CREDENTIALS_FILE, 'r') as f:
        creds = json.load(f)
        current_ssid = creds.get('ssid', 'Unknown')
except:
    current_ssid = 'Unknown'

print(f'[MAIN] Weather Station')
print(f'[MAIN] IP: {ip_address}')
print(f'[MAIN] Network: {current_ssid}')

# Setup BMP280 sensor
i2c = I2C(id=1, sda=Pin(2), scl=Pin(3))
bmp = BME280(i2c=i2c)
print('[MAIN] BMP280 initialized')


def delete_credentials():
    try:
        os.remove(CREDENTIALS_FILE)
        print('[MAIN] Credentials deleted')
    except:
        pass


def send_html_chunked(conn, content):
    """Send HTML response in chunks to avoid buffer overflow."""
    
    start_time = time.ticks_ms()
    
    conn.send('HTTP/1.1 200 OK\r\n')
    conn.send('Content-Type: text/html\r\n')
    conn.send('Connection: close\r\n\r\n')
    
    # Send in 512-byte chunks
    chunk_size = config.CHUNK_SIZE
    total_sent = 0
    
    for i in range(0, len(content), chunk_size):
        chunk = content[i:i+chunk_size]
        sent = conn.send(chunk)
        total_sent += sent
        
        # If partial send, retry the rest
        while sent < len(chunk):
            remaining = chunk[sent:]
            sent += conn.send(remaining)
            total_sent += sent
    
    end_time = time.ticks_ms()
    
    print(f"[HTTP] Sent {total_sent}/{len(content)} bytes in {end_time - start_time}ms")
    conn.close()


def get_sensor_html():
    """Read sensor data and generate HTML."""
    temp = bmp.temperature
    pressure = bmp.pressure
    
    try:
        temp_val = float(temp.replace('C', '').strip())
    except:
        temp_val = 0
    
    try:
        pres_val = float(pressure.replace('hPa', '').strip())
    except:
        pres_val = 0
    
    if temp_val > config.TEMP_HIGH:
        temp_color = '#ff4444'
        temp_status = 'HOT'
    elif temp_val < config.TEMP_LOW:
        temp_color = '#4444ff'
        temp_status = 'COLD'
    else:
        temp_color = '#44ff44'
        temp_status = 'NORMAL'
    
    if pres_val < config.PRESSURE_LOW:
        pres_color = '#ffaa00'
        pres_status = 'LOW'
    elif pres_val > config.PRESSURE_HIGH:
        pres_color = '#aa00ff'
        pres_status = 'HIGH'
    else:
        pres_color = '#44ff44'
        pres_status = 'NORMAL'
    
    return html.render(
        temp, temp_color, temp_status,
        pressure, pres_color, pres_status,
        ip_address, current_ssid
    )


# Create HTTP server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(addr)
server.listen(1)
print(f'[MAIN] Server: http://{ip_address}')

led_pin.on()

# Main loop
while True:
    try:
        conn, client_addr = server.accept()
        request = conn.recv(1024).decode()
        
        if 'GET /logout' in request:
            print('[MAIN] Logout requested')
            
            response = html.render_logout()
            send_html_chunked(conn, response)  # ← Use chunked sending
            
            time.sleep(1)
            delete_credentials()
            server.close()
            wlan.active(False)
            time.sleep(1)
            print('[MAIN] Switching to AP mode...')
            exec(open('booty.py').read())
            break
        
        elif 'GET /favicon' in request:
            conn.send('HTTP/1.1 204 No Content\r\n\r\n')
            conn.close()
        
        else:
            response = get_sensor_html()
            send_html_chunked(conn, response)  # ← Use chunked sending
        
        
    except Exception as e:
        print(f'[ERROR] {e}')
        try:
            conn.close()
        except:
            pass

    time.sleep_ms(50)