#!/usr/bin/env python3
"""
Development preview server.
Run this on your computer to preview templates in browser.
Usage: python3 dev_preview.py
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

# Base path for templates
TEMPLATE_DIR = "../src/templates"

# Sample data for previewing templates
PREVIEW_DATA = {
    "ERROR_HTML": "",
    "IP_PART_0": "192",
    "IP_PART_1": "168",
    "IP_PART_2": "1",
    "IP_LAST": "100",
    "IP_PREFIX": "192.168.1",
    "SSID": "MyWiFi",
    "FULL_IP": "192.168.1.100",
    "AP_SSID": "PicoW-Weatherstation",
    "TEMPERATURE": "22.5C",
    "TEMP_COLOR": "#44ff44",
    "TEMP_STATUS": "Comfortable",
    "PRESSURE": "1013.25hPa",
    "PRES_COLOR": "#44aaff",
    "PRES_STATUS": "Normal",
    "IP_ADDRESS": "192.168.1.100",
    "REFRESH_INTERVAL": "5",
}

def load_css():
    """Load CSS fresh each request for live editing."""
    try:
        with open(f"{TEMPLATE_DIR}/styles.css", 'r') as f:
            return f.read()
    except:
        return "/* CSS not found */"

class PreviewHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve template files with substitutions
        if self.path.endswith('.html'):
            template_path = f"{TEMPLATE_DIR}{self.path}"
            if os.path.exists(template_path):
                with open(template_path, 'r') as f:
                    html = f.read()
                
                # Load CSS fresh each time
                html = html.replace("{{CSS}}", load_css())
                
                # Replace all other placeholders
                for key, value in PREVIEW_DATA.items():
                    html = html.replace(f"{{{{{key}}}}}", str(value))
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html.encode())
                return
        
        # Default handler for other files
        super().do_GET()

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server = HTTPServer(('localhost', 8080), PreviewHandler)
    print("Preview server running at http://localhost:8080")
    print("Available pages:")
    for f in os.listdir(TEMPLATE_DIR):
        if f.endswith('.html'):
            print(f"  http://localhost:8080/{f}")
    print("\nCSS reloads on each request - just refresh browser!")
    server.serve_forever()