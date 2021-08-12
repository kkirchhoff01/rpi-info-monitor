#!/usr/bin/python3

import functools
import datetime
import requests
import psutil
from flask import Flask, Response, request
import socket
import json
import copy
import time

app = Flask(__name__)
timestamp = None

PORT = 5000


@functools.lru_cache(None)
def get_ip_info_cached():
    res = requests.get("https://ipleak.net/json/", verify=False)
    return res.json()


@functools.lru_cache(None)
def get_service_info_cached(service):
    procs = [p.name() for p in psutil.process_iter()]
    proc_count = len([p for p in procs if p == service])
    return proc_count, procs


def get_uptime_string():
    uptime = time.time() - psutil.boot_time()
    hr, mm = divmod(uptime / 60, 60)
    d, hr = divmod(hr, 24)
    return f'{d:,.0f}d {hr:.0f}h {mm:.0f}m'


def get_usage_info(format_string=True):
    mem = psutil.virtual_memory()
    used_gb = mem.used / 1e9
    total_gb = mem.total / 1e9

    cpu_pct = psutil.cpu_percent()

    if not format_string:
        return {
            'memory': {
                'used': used_gb,
                'total': total_gb,
                'percent': mem.percent
            },
            'cpu': {
                'percent': cpu_pct
            }
        }
    else:
        return {
            'memory':f'{used_gb:.1f}/{total_gb:.0f}GB '\
                f'({mem.percent:.1f}%)',
            'cpu': f'{cpu_pct:.1f}%',
        }


def _check_timestamp(refresh=5):
    global timestamp
    if timestamp is None:
        timestamp = datetime.datetime.now()

    timediff = (datetime.datetime.now() - timestamp)
    if (timediff.seconds / 60) >= refresh:
        # Cache will clear after refresh period is exceeded
        get_ip_info_cached.cache_clear()
        get_service_info_cached.cache_clear()
        timestamp = datetime.datetime.now()


def get_ip_info():
    _check_timestamp()
    return copy.deepcopy(get_ip_info_cached())


def get_service_info(services=('pihole-FTL', 'qbittorrent-nox')):
    _check_timestamp()

    service_info = []
    for service in services:
        proc_count, procs = get_service_info_cached(service)
        service_info.append({
            'name': service,
            'count': proc_count,
            'running': (proc_count > 0)
        })
    return copy.deepcopy(service_info)


@app.route('/api/info')
def server_info():
    try:
        ip_info = get_ip_info()
        services = request.args\
            .get('services')
        if services is not None:
            service_info = get_service_info(
                services=services.split(','),
            )
        else:
            service_info = get_service_info()

        res = {
            'ip_info': {
                'ip': ip_info.get('ip'),
                'state': ip_info.get('region_name'),
                'city': ip_info.get('city_name'),
            },
            'service_info': service_info,
            'uptime': get_uptime_string(),
            'usage': get_usage_info(),
        }

        return Response(
            json.dumps(res),
            status=200,
            content_type='application/json',
        )
    except Exception as e:
        return Response(str(e), status=500)


if __name__ == '__main__':
    app.run('0.0.0.0', PORT)
