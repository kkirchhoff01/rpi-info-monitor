from .config import (
    HOSTS,
    SERVICES,
    COUNT_DISPLAY_SERVICES,
    WIDTH,
    API_PORT,
    VALUE_SPACING,
)
import requests
import datetime
from typing import Union, List


ListOrStr = Union[List[str], str]


def timestring(width=WIDTH):
    _now = datetime.datetime.now()
    am_pm, hour = divmod(_now.time().hour, 12)
    if hour == 0 and am_pm:
        hour = 12
    minute = str(_now.time()).split(':')[1]
    formatted_time = f"{'0' if hour < 10 else ''}{hour}:"\
        f"{minute} {'PM' if am_pm else 'AM'}"
    curdate = str(_now).split(' ')[0]
    buffer_ = width - (len(curdate) + len(formatted_time))
    return curdate + ' '*buffer_ + formatted_time


def rotate(content: list,
           as_string: bool = False) -> ListOrStr:
    """Rotate the content text or list"""
    new_width = ((WIDTH + 1) * len(content) - 1)
    curtime = timestring(width=new_width)
    content_horizontal = [
        '-'*new_width,
        curtime,
        '-'*new_width,
        [
            '|'.join([
                r + ' '*(WIDTH - len(r))
                for r in row
            ])
            for row in zip(*content)
        ],
        '-'*new_width,
    ]

    if as_string:
        content_horizontal = '\n'.join([
            *content_horizontal[:3],
            '\n'.join(content_horizontal[3]),
            *content_horizontal[4:],
        ])

    return content_horizontal

def format_usage_str(resources):
    mem_str = resources['memory']
    cpu_str = resources['cpu']

    membuff = VALUE_SPACING - 13
    cpubuff = VALUE_SPACING - 10
    return [
        '-'*WIDTH,
        'Memory Usage:' + ' '*membuff + mem_str,
        'CPU Usage:' + ' '*cpubuff + cpu_str,
    ]


def get_content(show: bool = False,
                vertical: bool = True) -> ListOrStr:
    """Get content for display in a list or string"""

    curtime = timestring()
    display_content = [
        curtime,
        '-'*WIDTH,
    ]

    # Used only for horizontal format
    _display_content = []

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
            ])
            if not vertical:
                _display_content.append(display_content)
            else:
                display_content.append('\n')
            continue

        ip_info = status_content['ip_info']
        service_info = status_content['service_info']
        uptime = status_content.get('uptime', '')
        usage = status_content.get('usage')
        
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
            buffer_ = " "*(VALUE_SPACING - len(s_title))
            display_content.append(f'{s_title}{buffer_}{status}')

        if usage is not None:
            display_content.extend(format_usage_str(usage))
        else:
            if not vertical:
                display_content.append('-'*WIDTH)
            else:
                display_content.append('')
            display_content.extend(['']*2)

        if not vertical:
            _display_content.append(display_content)
        else:
            display_content.append('\n')

    if not vertical:
        display_content = _display_content[:]

    if show:
        print('\n'.join(display_content))

    return display_content
