#-------------------
# Boot Script
# Manages Wi-Fi connection or Access Point mode.
#-------------------

import sys
import os
import network
import time
import json
import socket
from machine import Pin
import config
import html


# ==================
# Constants
# ==================

CREDENTIALS_FILE = 'credentials.json'
STAT_GOT_IP = 3


# ==================
# Globals
# ==================

led = Pin('LED', Pin.OUT)
sta = network.WLAN(network.STA_IF)
ap = network.WLAN(network.AP_IF)

sta.active(False)
ap.active(False)


# ==================
# LED Utilities
# ==================

def blink(times, speed=200):
    """Blink LED a number of times."""
    for _ in range(times):
        led.on()
        time.sleep_ms(speed)
        led.off()
        time.sleep_ms(speed)


# ==================
# Credentials
# ==================

def load_credentials():
    """Load saved WiFi credentials."""
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def save_credentials(ssid, password, static_ip):
    """Save WiFi credentials to file."""
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump({
            'ssid': ssid,
            'password': password,
            'static_ip': static_ip
        }, f)


def delete_credentials():
    """Remove saved credentials file."""
    try:
        os.remove(CREDENTIALS_FILE)
    except OSError:
        pass


# ==================
# HTTP Helpers
# ==================

def send_html(conn, content):
    """Send HTML response in chunks."""
    conn.send('HTTP/1.1 200 OK\r\n')
    conn.send('Content-Type: text/html\r\n')
    conn.send('Connection: close\r\n\r\n')
    
    # Send in 512-byte chunks to avoid buffer overflow
    chunk_size = 512
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
    
    print(f"[HTTP] Sent {total_sent}/{len(content)} bytes")
    conn.close()


def send_redirect(conn, location):
    """Send redirect response."""
    conn.send('HTTP/1.1 302 Found\r\n')
    conn.send(f'Location: {location}\r\n')
    conn.send('Connection: close\r\n\r\n')
    conn.close()


def url_decode(s):
    """Decode URL-encoded string."""
    result = s.replace('+', ' ')
    parts = result.split('%')
    decoded = parts[0]
    for part in parts[1:]:
        try:
            decoded += chr(int(part[:2], 16)) + part[2:]
        except ValueError:
            decoded += '%' + part
    return decoded


# ==================
# Network Functions
# ==================

def start_station_mode(ssid, password, static_ip=None, timeout=15, keep_ap=False):
    """Connect to Wi-Fi network.
    
    Returns IP address on success, None on failure.
    """
    global sta, ap
    
    if not keep_ap:
        ap.active(False)
    
    sta.active(False)
    time.sleep_ms(100)
    sta.active(True)
    
    ip_to_use = static_ip or config.STATIC_IP
    
    if config.USE_STATIC_IP:
        sta.ifconfig((ip_to_use, config.SUBNET_MASK, config.GATEWAY, config.DNS))
        print(f'[WIFI] Static IP: {ip_to_use}')
    
    print(f'[WIFI] Connecting to {ssid}...')
    sta.connect(ssid, password)
    
    for _ in range(timeout):
        if sta.status() == STAT_GOT_IP:
            ip = sta.ifconfig()[0]
            print(f'[WIFI] Connected! IP: {ip}')
            return ip
        led.toggle()
        time.sleep(1)
    
    sta.active(False)
    return None


def start_ap_mode():
    """Start Access Point and serve setup page."""
    global sta, ap
    
    sta.active(False)
    ap.active(True)
    
    if config.AP_PASSWORD:
        ap.config(essid=config.AP_SSID, password=config.AP_PASSWORD)
    else:
        ap.config(essid=config.AP_SSID, security=0)
    
    while not ap.active():
        time.sleep(0.5)
    
    print(f'[AP] Started: {config.AP_SSID}')
    print(f'[AP] Open: http://192.168.4.1')
    
    serve_setup_page()


# ==================
# Main Server
# ==================

def serve_setup_page():
    """Serve Wi-Fi configuration page."""
    
    ip_parts = config.STATIC_IP.split('.')
    ip_prefix = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}"
    
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(addr)
    server.listen(1)

    # State
    pending_creds = None    # Verified credentials awaiting confirmation
    show_error = False      # Show error on next page load
    testing_creds = None    # Credentials being tested
    
    while True:
        try:
            conn, addr = server.accept()
            request = conn.recv(1024).decode()
            
            # ===== User submits form =====
            if 'GET /save?' in request:
                params = request.split('GET /save?')[1].split(' ')[0]
                pairs = params.split('&')
                form_data = {}
                for pair in pairs:
                    if '=' in pair:
                        key, value = pair.split('=', 1)
                        form_data[key] = url_decode(value)
                
                ip_last = form_data.get('ip_last', ip_parts[3])
                full_ip = f"{ip_prefix}.{ip_last}"
                
                testing_creds = {
                    'ssid': form_data.get('ssid', ''),
                    'password': form_data.get('password', ''),
                    'static_ip': full_ip
                }
                
                send_redirect(conn, '/connecting')
                continue
            
            # ===== Show connecting page, then test =====
            elif 'GET /connecting' in request:
                if testing_creds:
                    # Show connecting page
                    send_html(conn, html.render_connecting(testing_creds['ssid']))
                    
                    print(f'[AP] Testing: {testing_creds["ssid"]} @ {testing_creds["static_ip"]}')
                    
                    # Close server during test
                    server.close()
                    
                    # Test connection
                    ip = start_station_mode(
                        testing_creds['ssid'],
                        testing_creds['password'],
                        testing_creds['static_ip'],
                        keep_ap=True
                    )
                    
                    # Recreate server
                    server = socket.socket()
                    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    server.bind(socket.getaddrinfo('0.0.0.0', 80)[0][-1])
                    server.listen(1)
                    
                    led.off()
                    
                    if ip:
                        print('[AP] Test successful!')
                        pending_creds = testing_creds
                        sta.active(False)  # Disconnect STA, keep AP
                    else:
                        print('[AP] Connection failed!')
                        show_error = True
                    
                    testing_creds = None
                    continue
                else:
                    send_redirect(conn, '/')
                    continue
            
            # ===== User confirms connection =====
            elif 'GET /confirm' in request:
                if pending_creds:
                    print('[AP] Confirmed! Saving and starting main...')
                    
                    save_credentials(
                        pending_creds['ssid'],
                        pending_creds['password'],
                        pending_creds['static_ip']
                    )
                    
                    send_html(conn, html.render_success(pending_creds['static_ip']))
                    
                    time.sleep(2)
                    
                    server.close()
                    ap.active(False)
                    
                    ip = start_station_mode(
                        pending_creds['ssid'],
                        pending_creds['password'],
                        pending_creds['static_ip']
                    )
                    
                    if ip:
                        blink(3, 100)
                        led.on()
                        if 'maing' in sys.modules:
                            del sys.modules['maing']
                        exec(open('maing.py').read())
                    return
                else:
                    send_redirect(conn, '/')
                    continue

            # ===== User cancels =====
            elif 'GET /cancel' in request:
                print('[AP] Cancelled')
                pending_creds = None
                testing_creds = None
                show_error = False
                send_redirect(conn, '/')
                continue

            # ===== Favicon =====
            elif 'favicon' in request:
                conn.send('HTTP/1.1 204 No Content\r\n\r\n')
                conn.close()
            
            # ===== Main page =====
            else:
                if pending_creds:
                    send_html(conn, html.render_confirm(
                        pending_creds['ssid'],
                        pending_creds['static_ip']
                    ))
                elif show_error:
                    send_html(conn, html.render_setup("Connection failed! Check SSID and password."))
                    show_error = False
                else:
                    send_html(conn, html.render_setup())
            
            led.toggle()
            
        except Exception as e:
            print(f'[AP ERROR] {e}')
            try:
                conn.close()
            except:
                pass


# ==================
# Boot Entry Point
# ==================

print('\n[BOOT] Pico W Weather Station')
print('[BOOT] ========================')
blink(2)

creds = load_credentials()

if creds:
    print(f'[BOOT] Found: {creds["ssid"]}')
    static_ip = creds.get('static_ip', config.STATIC_IP)
    ip = start_station_mode(creds['ssid'], creds['password'], static_ip)
    
    if ip:
        blink(3, 100)
        led.on()
        exec(open('maing.py').read())
    else:
        print('[BOOT] Connection failed')
        delete_credentials()
        blink(5, 500)
        start_ap_mode()
else:
    print('[BOOT] No saved credentials')
    start_ap_mode()