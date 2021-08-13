# rpi-info-monitor
Display information for multiple raspberry pi's in the console

## Install:
-----------
To install the flask service on each pi, run the `install.sh` script (as root).

To display the content from the API call use the `display.sh` script or `display` module in the repo directory.

Before running the display, modify the `HOSTS` variable in `display/config.py` to include the host/IP for each pi

## Examples:
-----------
#### Command:

`$ ./display.sh` or `$ python3 -m display`

#### Output:

![rpi-monitor-example](https://user-images.githubusercontent.com/8592588/129414337-fb6f08c3-ef57-4323-9f88-2c88181b79f9.png)

#### Web Output:
<pre>
-----------------------------------------------------------------------------------------------------------------
2021-08-13                                                                                               04:13 PM
-----------------------------------------------------------------------------------------------------------------
rpi - 192.168.1.1                    |rpi2 - 192.168.1.2                   |rpi3 - 192.168.1.3
-------------------------------------|-------------------------------------|-------------------------------------
Status: Up (4d 6h 29m)               |Status: Up (0d 17h 15m)              |Status: Up (7d 1h 55m)
-------------------------------------|-------------------------------------|-------------------------------------
IP:               x.x.x.x            |IP:               x.x.x.x            |IP:               x.x.x.x
IP State:         Pennsylvania       |IP State:         New York           |IP State:         Pennsylvania
IP City:          Philadelphia       |IP City:          New York           |IP City:          Philadelphia
-------------------------------------|-------------------------------------|-------------------------------------
pihole-FTL:       Running            |pihole-FTL:       Stopped            |pihole-FTL:       Running
openvpn:          Stopped            |openvpn:          Running            |openvpn:          Stopped
qbittorrent-nox:  0 Services         |qbittorrent-nox:  2 Services         |qbittorrent-nox:  0 Services
dockerd:          Running            |dockerd:          Stopped            |dockerd:          Stopped
minidlnad:        Running            |minidlnad:        Stopped            |minidlnad:        Stopped
sshfs:            2 Services         |sshfs:            2 Services         |sshfs:            0 Services
-------------------------------------|-------------------------------------|-------------------------------------
Memory Usage:     0.3/4.1GB (13.4%)  |Memory Usage:     0.1/1.9GB (13.5%)  |Memory Usage:     0.2/1.0GB (26.3%)
CPU Usage:        2.6%               |CPU Usage:        0.2%               |CPU Usage:        0.1%
CPU Temp:         45.8C              |CPU Temp:         37.5C              |CPU Temp:         39.7C
-----------------------------------------------------------------------------------------------------------------
</pre>

#### Command:

`$ ./display.sh --vertical` or`$ python3 -m display --vertical` (or replace `--vertical` with `-v`)

#### Output:

![rpi-monitor-example-vertical](https://user-images.githubusercontent.com/8592588/129414343-d500b733-a76c-47dd-9675-bf3947f705bf.png)

#### Web Output:

<pre>
2021-08-13                   04:14 PM
-------------------------------------
rpi - 192.168.1.1
-------------------------------------
Status: Up (4d 6h 29m)
-------------------------------------
IP:               x.x.x.x
IP State:         Pennsylvania
IP City:          Philadelphia
-------------------------------------
pihole-FTL:       Running
openvpn:          Stopped
qbittorrent-nox:  0 Services
dockerd:          Running
minidlnad:        Running
sshfs:            2 Services
-------------------------------------
Memory Usage:     0.3/4.1GB (13.4%)
CPU Usage:        1.1%
CPU Temp:         44.8C


rpi2 - 192.168.1.2
-------------------------------------
Status: Up (0d 17h 15m)
-------------------------------------
IP:               x.x.x.x
IP State:         New York
IP City:          New York
-------------------------------------
pihole-FTL:       Stopped
openvpn:          Running
qbittorrent-nox:  2 Services
dockerd:          Stopped
minidlnad:        Stopped
sshfs:            2 Services
-------------------------------------
Memory Usage:     0.1/1.9GB (13.5%)
CPU Usage:        0.4%
CPU Temp:         38.5C


rpi3 - 192.168.1.3
-------------------------------------
Status: Up (7d 1h 56m)
-------------------------------------
IP:               x.x.x.x
IP State:         Pennsylvania
IP City:          Philadelphia
-------------------------------------
pihole-FTL:       Running
openvpn:          Stopped
qbittorrent-nox:  0 Services
dockerd:          Stopped
minidlnad:        Stopped
sshfs:            0 Services
-------------------------------------
Memory Usage:     0.2/1.0GB (26.3%)
CPU Usage:        0.0%
CPU Temp:         39.7C
</pre>
