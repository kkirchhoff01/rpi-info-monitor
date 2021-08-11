#!/usr/bin/python3

import requests
import time
import subprocess
import datetime
import argparse
from typing import Union, List

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

ListOrStr = Union[List[str], str]


def rotate(content: list,
           as_string: bool = False) -> ListOrStr:
    """Rotate the content text or list"""
    content_vert = [
        '-'*(36*len(content)-1),
        [
            '|'.join([
                r + ' '*(WIDTH - len(r))
                for r in row
            ])
            for row in zip(*content)
        ],
        '-'*(36*len(content)-1),
    ]

    if as_string:
        content_vert = '\n'.join([
            content_vert[0],
            '\n'.join(content_vert[1]),
            content_vert[2],
        ])

    return content_vert


def get_content(show: bool = False,
                vertical: bool = True) -> ListOrStr:
    """Get content for display in a list or string"""
    dt, _ = str(datetime.datetime.now())\
        .split('.')

    display_content = [
        dt.replace(' ', ' '*17),
        '-'*WIDTH,
    ]

    # Used only for horizontal format
    _display_content = []
    if not vertical:
        display_content = [display_content]

    for pi_info in HOSTS:
        # Populate seperate lists for each
        # host to allow for rotation
        # from `_display_content`
        if not vertical:
            display_content = []
        hostname = pi_info['hostname']
        local_ip = pi_info['local_ip']
        try:
            services = ','.join(SERVICES)
            status_content = requests.get(
                f'http://{local_ip}:{API_PORT}/api/info'
                f'?services={services}',
            )
            status_content = status_content.json()
        except Exception:
            display_content.extend([
                f'{hostname} - {local_ip}',
                '-'*WIDTH,
                'Status: Down',
                '-'*WIDTH,
                f'IP:               N/A',
                f'IP State:         N/A',
                f'IP City:          N/A',
                '-'*WIDTH,
                '\n',
            ])
            if not vertical:
                _display_content.append(display_content)
            continue

        ip_info = status_content['ip_info']
        service_info = status_content['service_info']
        uptime = status_content.get('uptime', '')
        if uptime:
            uptime = f'({uptime})'

        display_content.extend([
            f'{hostname} - {local_ip}',
            '-'*WIDTH,
            f'Status: Up {uptime}',
            '-'*WIDTH,
            f'IP:               {ip_info["ip"]}',
            f'IP State:         {ip_info["state"]}',
            f'IP City:          {ip_info["city"]}',
            '-'*WIDTH,
        ])
        for service in service_info:
            s_title = f'{service["name"]}:'
            if service["name"] in COUNT_DISPLAY_SERVICES:
                status = (f'{service["count"]} Services')
            else:
                status = (
                    'Running' if service['running']
                    else 'Stopped'
                )
            buffer_ = " "*(18 - len(s_title))
            display_content.append(f'{s_title}{buffer_}{status}')

        if not vertical:
            _display_content.append(display_content)
        else:
            display_content.append('\n')

    if not vertical:
        display_content = _display_content[:]

    if show:
        print('\n'.join(display_content))

    return display_content


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--run-forever',
        '--run', '-r',
        action='store_true',
    )
    argparser.add_argument(
        '--vertical',
        '-v',
        action='store_true',
    )
    args = argparser.parse_args()

    # If run_forever is True, run an
    # infinite loop (e.g. `while True:`)
    while args.run_forever:
        try:
            content = get_content(vertical=args.vertical)
            if not args.vertical:
                content = rotate(content, as_string=True)
            else:
                content = '\n'.join(content)
            _ = subprocess.call('clear', shell=True)
            print(content)
            time.sleep(5)
        except KeyboardInterrupt:
            break
    else:
        content = get_content(vertical=args.vertical)
        if not args.vertical:
            content = rotate(content, as_string=True)
        else:
            content = '\n'.join(content)
        print(content)
