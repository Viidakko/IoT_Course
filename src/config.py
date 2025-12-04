#-------------------
# Configuration File
#-------------------

# Access Point settings
AP_SSID = 'PicoW-Weatherstation'
AP_PASSWORD = '' 

# Static IP settings
USE_STATIC_IP = True
STATIC_IP = '192.168.1.100'
SUBNET_MASK = '255.255.255.0'
GATEWAY = '192.168.1.1'
DNS = '8.8.8.8'

# Web server settings
REFRESH_INTERVAL = 5

# Sensor thresholds
TEMP_HIGH = 25.0
TEMP_LOW = 18.0
PRESSURE_LOW = 1000
PRESSURE_HIGH = 1020