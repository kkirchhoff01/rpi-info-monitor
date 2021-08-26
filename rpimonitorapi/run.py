#!/usr/bin/python3

from functools import lru_cache
import datetime
import requests
import psutil
from flask import Flask, Response, request
from typing import Dict, List, Union
import json
import time

app = Flask(__name__)
timestamp = None


PORT = 5000
CACHE_TIME = 2
PROC_CACHE = 30


class _Process:
    def __init__(self,
                 name: str,
                 status_only: bool = True):
        self.name = name
        self.status_only = status_only
        self._procs = []
        self.count = 0
        self._timestamp = datetime.datetime.now()

    def initialize(self):
        self._timestamp = datetime.datetime.now()
        self._procs = [
            p for p in psutil.process_iter()
            if p.name().lower() == self.name.lower()
        ]

        self.count = len(self._procs)

    def _update(self):
        if self.count == 0:
            last_refresh = (
                datetime.datetime.now() -
                    self._timestamp
            )
            if last_refresh.seconds / 60 >= CACHE_TIME:
                self.initialize()
            return
        
        refresh = any(
            p for p in self._procs
            if not p.is_running()
        )
        # Only refresh when
        # process status has changed
        if refresh:
            self.initialize()

    @property
    def running(self) -> Union[bool, int]:
        self._update()
        if self.status_only:
            return self.count > 0
        else:
            return self.count

    def get_info(self) -> Dict[str, object]:
        # Call `running` first to make
        # sure count is updated
        _running = self.running
        return {
            'name': self.name,
            'running': _running,
            'count': self.count,
        }

    def __str__(self):
        if self.status_only:
            return (
                'Running' if self.running
                else 'Stopped'
            )
        else:
            return f'{self.running} Services'

class ProcessCache:
    def __init__(self):
        self.processes = {}
        self._timestamp = datetime.datetime.now()

    def add(self, name):
        if name.lower() in self.processes:
            return
        proc = _Process(name)
        proc.initialize()
        self.processes[name.lower()] = proc

    def _check_timestamp(self):
        # Periodic refresh for each process
        last_refresh = (
            datetime.datetime.now() -
                self._timestamp
        )
        if last_refresh.seconds / 60 >= PROC_CACHE:
            self.reset()

    def reset(self):
        self._timestamp = datetime.datetime.now()
        for proc in self.processes.values():
            proc.initialize()

    def get(self, name, info_dict=True):
        self._check_timestamp()
        
        if name.lower() not in self.processes:
            self.add(name)

        curproc = self.processes[name.lower()]
        if info_dict:
            return curproc.get_info()
        else:
            return curproc

proc_cache = ProcessCache()


@lru_cache(None)
def get_ip_info_cached():
    res = requests.get("https://ipleak.net/json/", verify=False)
    return res.json()


def get_uptime_string():
    uptime = time.time() - psutil.boot_time()
    hr, mm = divmod(uptime / 60, 60)
    d, hr = divmod(hr, 24)
    return f'{d:,.0f}d {hr:.0f}h {mm:.0f}m'


def get_usage_info(format_string=True, fahrenheit=True):
    mem = psutil.virtual_memory()
    used_gb = mem.used / 1e9
    total_gb = mem.total / 1e9

    cpu_pct = psutil.cpu_percent()

    temp_info_ = psutil.sensors_temperatures(
        fahrenheit=fahrenheit,
    )
    temp_info = {}
    if len(temp_info_) == 0:
        temp_info['temp'] = 'N/A'
        temp_info['units'] = ''
    else:
        curtemp = list(temp_info_.values())[0]
        if len(curtemp) > 0:
            curtemp = curtemp[0].current
        else:
            curtemp = -1
        temp_info['temp'] = round(curtemp, 1)
        temp_info['units'] = ('F' if fahrenheit else 'C')

    if not format_string:
        return {
            'memory': {
                'used': used_gb,
                'total': total_gb,
                'percent': mem.percent
            },
            'cpu': {
                'percent': cpu_pct
            },
            'temp': temp_info
        }
    else:
        return {
            'memory':f'{used_gb:.1f}/{total_gb:.0f}GB '\
                f'({mem.percent:.1f}%)',
            'cpu': f'{cpu_pct:.1f}%',
            'temp': f'{temp_info["temp"]}{temp_info["units"]}'
        }


def _check_timestamp(refresh=CACHE_TIME):
    global timestamp
    if timestamp is None:
        timestamp = datetime.datetime.now()

    timediff = (datetime.datetime.now() - timestamp)
    if (timediff.seconds / 60) >= refresh:
        # Cache will clear after refresh period is exceeded
        get_ip_info_cached.cache_clear()
        timestamp = datetime.datetime.now()


def get_ip_info() -> Dict[str, str]:
    _check_timestamp()

    ip_info = get_ip_info_cached()
    return ip_info


def get_service_info(
        services=('pihole-FTL', 'qbittorrent-nox'),
        ) -> List[Dict[str, object]]:
    service_info = []
    for service in services:
        proc = proc_cache.get(service, info_dict=True)
        service_info.append({
            'name': service,
            'count': proc['count'],
            'running': proc['running'],
        })
    return service_info


@app.route('/api/clear-cache')
def clear_cache():
    try:
        get_ip_info_cached.cache_clear()
        proc_cache.reset()
        return Response(status=200)
    except Exception as e:
        return Response(str(e), status=500)


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

        format_usage = request.args\
            .get('format_usage', True)
        if isinstance(format_usage, str):
            format_usage = (
                True if format_usage.lower() 
                    in ('true', '1')
                else False
            )
        temp_units = request.args\
            .get('temp_units', 'fahrenheit')
        fahrenheit = (temp_units.lower() == 'fahrenheit')

        res = {
            'ip_info': {
                'ip': ip_info.get('ip'),
                'state': ip_info.get('region_name'),
                'city': ip_info.get('city_name'),
            },
            'service_info': service_info,
            'uptime': get_uptime_string(),
            'usage': get_usage_info(
                format_usage,
                fahrenheit=fahrenheit,
            ),
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
