
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

# Width of display
WIDTH = 35
API_PORT = 5000

__all__ = [
    'HOSTS',
    'SERVICES',
    'COUNT_DISPLAY_SERVICES',
    'WIDTH',
    'API_PORT',
]
