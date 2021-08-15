
# Add all host/ip info for each pi
HOSTS = [
    {
        'hostname': 'rpi1',
        'local_ip': '192.168.1.1',
    },
    {
        'hostname': 'rpi2',
        'local_ip': '192.168.1.2',
    },
]

# Services you want to monitor
SERVICES = [
    'pihole-FTL',
    'openvpn',
    'qbittorrent-nox',
    'dockerd',
    'minidlnad',
    'sshfs',
]

# These will show the number or services
# running instead or 'Running'/'Stopped'
COUNT_DISPLAY_SERVICES = [
    'qbittorrent-nox',
    'sshfs',
]

VALID_STYLES = [
    '\x1b[1m',
    '\x1b[0m',
    '\x1b[91m',
    '\x1b[95m',
    '\x1b[94m',
    '\x1b[96m',
    '\x1b[92m',
    '\x1b[4m',
    '\x1b[93m',
]

# Width of display
WIDTH = 37
VALUE_SPACING = 18
API_PORT = 5000
SLEEP_TIME = 5
PCT_RED_THRESH = 80.0
TEMP_UNITS = 'celsius'
MAX_TEMP = 185.0

__all__ = [
    'HOSTS',
    'SERVICES',
    'COUNT_DISPLAY_SERVICES',
    'WIDTH',
    'API_PORT',
    'SLEEP_TIME',
    'VALUE_SPACING',
    'PCT_RED_THRESH',
    'VALID_STYLES',
    'TEMP_UNITS',
    'MAX_TEMP',
]
