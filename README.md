# rpi-info-monitor
Display information for multiple raspberry pi's in the console

## Example:
-----------
#### Command:

`$ ./display.py`

#### Output:

<pre>
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
</pre>
