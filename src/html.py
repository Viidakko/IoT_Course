#-------------------
# Template Engine
# Loads HTML templates and CSS, handles variable substitution.
#-------------------

import config

# Cache CSS at module load
_CSS_CACHE = None

def load_css():
    """Load CSS file once and cache."""
    global _CSS_CACHE
    if _CSS_CACHE is None:
        try:
            with open("templates/styles.css", "r") as f:
                _CSS_CACHE = f.read()
        except:
            _CSS_CACHE = "/* CSS not found */"
    return _CSS_CACHE


def load_template(name, **variables):
    """Load HTML template and substitute variables."""
    try:
        with open(f"templates/{name}", "r") as f:
            html = f.read()
    except:
        return f"<h1>Error loading template: {name}</h1>"
    
    # Replace CSS placeholder
    html = html.replace("{{CSS}}", load_css())
    
    # Replace all variables
    for key, value in variables.items():
        html = html.replace(f"{{{{{key}}}}}", str(value))
    
    return html


# ========== Setup/AP Pages ==========

def render_setup(error=None):
    """Render Wi-Fi setup page."""
    ip_parts = config.STATIC_IP.split('.')
    
    return load_template("setup.html",
        ERROR_HTML=f'<div class="error">{error}</div>' if error else '',
        IP_PART_0=ip_parts[0],
        IP_PART_1=ip_parts[1],
        IP_PART_2=ip_parts[2],
        IP_LAST=ip_parts[3],
        IP_PREFIX=f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}"
    )


def render_connecting(ssid):
    """Render connecting/testing page."""
    return load_template("connectingpage.html", SSID=ssid)


def render_confirm(ssid, full_ip):
    """Render connection confirmation page."""
    return load_template("connectconfirm.html",
        SSID=ssid,
        FULL_IP=full_ip,
        AP_SSID=config.AP_SSID
    )


def render_success(full_ip):
    """Render success page after saving credentials."""
    return load_template("connectconfirmed.html",
        FULL_IP=full_ip,
        AP_SSID=config.AP_SSID
    )


# ========== Weather Station Pages ==========

def render(temp, temp_color, temp_status, pressure, pres_color, pres_status, ip_address, ssid):
    """Render weather station dashboard."""
    return load_template("weather.html",
        TEMPERATURE=temp,
        TEMP_COLOR=temp_color,
        TEMP_STATUS=temp_status,
        PRESSURE=pressure,
        PRES_COLOR=pres_color,
        PRES_STATUS=pres_status,
        IP_ADDRESS=ip_address,
        SSID=ssid,
        REFRESH_INTERVAL=str(config.REFRESH_INTERVAL)
    )


def render_logout():
    """Render logout confirmation page."""
    return load_template("logout.html", AP_SSID=config.AP_SSID)