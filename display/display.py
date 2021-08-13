from config import (
    HOSTS,
    SERVICES,
    COUNT_DISPLAY_SERVICES,
    WIDTH,
    API_PORT,
    VALUE_SPACING,
    PCT_RED_THRESH,
    VALID_STYLES,
)
import requests
import datetime
from typing import Union, List


ListOrStr = Union[List[str], str]


class Styles:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    GREEN = OKGREEN = '\033[92m'
    YELLOW = WARNING = '\033[93m'
    RED = FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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


def _get_len(row):
    row = row[:]
    for s in VALID_STYLES:
        row = row.replace(s, '')
    return len(row)


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
                r + ' '*(WIDTH - _get_len(r))
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


def format_usage_str(resources, colored=True):
    mem_info = resources['memory']
    cpu_info = resources['cpu']

    mem_str = 'Memory Usage:'
    membuff = VALUE_SPACING - len(mem_str)
    mem_str += ' ' * membuff

    cpu_str = 'CPU Usage:'
    cpubuff = VALUE_SPACING - len(cpu_str)
    cpu_str += ' ' * cpubuff

    if colored:
        mem_color = (
            Styles.RED if mem_info['percent'] > PCT_RED_THRESH
            else Styles.GREEN
        )
        mem_str += mem_color
        cpu_color = (
            Styles.RED if cpu_info['percent'] > PCT_RED_THRESH
            else Styles.GREEN
        )
        cpu_str += cpu_color

    mem_str += f'{mem_info["used"]:,.1f}'\
        f'/{mem_info["total"]:,.1f}GB '\
        f'({mem_info["percent"]:.1f}%)'
    cpu_str += f'{cpu_info["percent"]:.1f}%'

    mem_str += (WIDTH - _get_len(mem_str)) * ' '
    cpu_str += (WIDTH - _get_len(cpu_str)) * ' '

    if colored:
        mem_str += Styles.ENDC
        cpu_str += Styles.ENDC

    return [
        '-'*WIDTH,
        mem_str,
        cpu_str,
    ]


def format_service_str(service, colored=True):
    s_title = f'{service["name"]}:'
    if service["name"] in COUNT_DISPLAY_SERVICES:
        status = (f'{service["count"]} Services')
        if colored:
            status = (
                Styles.GREEN if service['count'] > 0
                else Styles.RED
            ) + status + Styles.ENDC
    else:
        status = (
            'Running' if service['running']
            else 'Stopped'
        )
        if colored:
            status = (
                Styles.GREEN if status == 'Running'
                else Styles.RED
            ) + status + Styles.ENDC

    buffer_ = " "*(VALUE_SPACING - len(s_title))

    return f'{s_title}{buffer_}{status}'


def format_ip_info(ip_info):
    formatted = []
    ip, state, city = 'IP:', 'IP State:', 'IP City:'
    ip += (VALUE_SPACING - len(ip)) * ' '
    state += (VALUE_SPACING - len(state)) * ' '
    city += (VALUE_SPACING - len(city)) * ' '
    if ip_info is None:
        return [
            f'{ip}N/A',
            f'{state}N/A',
            f'{city}N/A',
        ]

    ip += ip_info['ip']
    state += ip_info['state']
    city += ip_info['city']

    return [ip, state, city]


def get_content(show: bool = False,
                vertical: bool = True,
                colored: bool = True) -> ListOrStr:
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
        if colored:
            header = f'{Styles.OKBLUE}{Styles.BOLD}{hostname} - '\
                f'{local_ip}{Styles.ENDC*2}'
        else:
            header = f'{hostname} - {local_ip}'
        try:
            services = ','.join(SERVICES)
            status_content = requests.get(
                f'http://{local_ip}:{API_PORT}/api/info'
                f'?services={services}'
                f'&format_usage=false',
            )
            status_content = status_content.json()
        except Exception:
            display_content.extend([
                header,
                '-'*WIDTH,
                'Status: Down',
                '-'*WIDTH,
                *format_ip_info(None),
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
            header,
            '-'*WIDTH,
            f'Status: Up {uptime}',
            '-'*WIDTH,
            *format_ip_info(ip_info),
            '-'*WIDTH,
        ])

        for service in service_info:
            display_content.append(
                format_service_str(
                    service,
                    colored=colored,
                ),
            )

        if usage is not None:
            display_content.extend(
                format_usage_str(usage, colored=colored),
            )
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
