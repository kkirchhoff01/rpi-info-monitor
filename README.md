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

<pre>
-----------------------------------------------------------------------------------------------------------
2021-08-12                                                                                         05:59 PM
-----------------------------------------------------------------------------------------------------------
rpi1- 192.168.1.1                  |rpi2 - 192.168.1.2                 |rpi3 - 192.168.1.3
-----------------------------------|-----------------------------------|-----------------------------------
Status: Up (2d 1h 57m)             |Status: Up (7d 22h 26m)            |Status: Up (4d 21h 23m)
-----------------------------------|-----------------------------------|-----------------------------------
IP:               x.x.x.x          |IP:               x.x.x.x          |IP:               x.x.x.x
IP State:         Pennsylvania     |IP State:         New York         |IP State:         Pennsylvania
IP City:          Philadelphia     |IP City:          New York         |IP City:          Philadelphia
-----------------------------------|-----------------------------------|-----------------------------------
pihole-FTL:       Running          |pihole-FTL:       Stopped          |pihole-FTL:       Running
openvpn:          Stopped          |openvpn:          Running          |openvpn:          Stopped
qbittorrent-nox:  0 Services       |qbittorrent-nox:  2 Services       |qbittorrent-nox:  0 Services
dockerd:          Running          |dockerd:          Stopped          |dockerd:          Stopped
minidlnad:        Running          |minidlnad:        Stopped          |minidlnad:        Stopped
sshfs:            2 Services       |sshfs:            2 Services       |sshfs:            0 Services
-----------------------------------------------------------------------------------------------------------
Memory Usage:     0.3/4GB (12.7%)  |Memory Usage:     0.4/2GB (28.4%)  |Memory Usage:     0.2/1GB (26.2%)  
CPU Usage:        0.3%             |CPU Usage:        24.1%            |CPU Usage:        0.1%             
-----------------------------------------------------------------------------------------------------------
</pre>

#### Command:

`$ ./display.sh --vertical` or`$ python3 -m display --vertical` (or replace `--vertical` with `-v`)

#### Output:

<pre>
2021-08-12                 05:59 PM
-----------------------------------
rpi1 - 192.168.1.1
-----------------------------------
Status: Up (2d 2h 60m)
-----------------------------------
IP:               x.x.x.x
IP State:         Pennsylvania
IP City:          Philadelphia
-----------------------------------
pihole-FTL:       Running
qbittorrent-nox:  0 Services
dockerd:          Running
minidlnad:        Running
sshfs:            2 Services


rpi2 - 192.168.1.2
-----------------------------------
Status: Up (7d 23h 29m)
-----------------------------------
IP:               x.x.x.x
IP State:         New York
IP City:          New York
-----------------------------------
pihole-FTL:       Stopped
qbittorrent-nox:  2 Services
dockerd:          Stopped
minidlnad:        Stopped
sshfs:            2 Services


rpi3 - 192.168.1.3
-----------------------------------
Status: Up (4d 22h 26m)
-----------------------------------
IP:               x.x.x.x
IP State:         Pennsylvania
IP City:          Philadelphia
-----------------------------------
pihole-FTL:       Running
qbittorrent-nox:  0 Services
dockerd:          Stopped
minidlnad:        Stopped
sshfs:            0 Services
</pre>
