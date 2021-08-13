# rpi-info-monitor
A simple, configurable application and set of services to monitor multiple raspberry pi's on a network. It can be used in a terminal or a web UI.

There are three components:
 1. `rpimonitorapi` - A flask API that runs on each pi to communicate information about the running proccesses and resources
 2. `display` - A module used to format and display the information about each pi into a terminal or web UI (can be viewed vertically or horizontally)
 3. `webdisplay` - A flask service that can be used to host the front end web UI. It can be installed on the main pi or another machine, but is not required
    
    
NOTE: The web UI (`webdisplay`) depends on the `display` module. It is suggested to keep these two folders in the same directory if you want to run the web UI. Otherwise you will need to add the `display` module contents to your PYTHONPATH

## Installation/Usage:
----------------------
 1. Install the flask service on each pi by running the `install.sh` script as root or setting up the services manually
 3. On your main pi/machine that will be used to run the display, modify the `HOSTS` variable in `display/config.py` with the host names and local IPs of your pi's
 4. Install the required python modules on the main pi/machine (`pip install -r requirements.txt`)
 5. You can then install the `rpi-info-webapi` service if you want to use the web UI (if using the web UI, you can get better formatting for mobile by installing the `flask_mobility` package)
 6. To run the display loop in a terminal, use `python3 -m display --run-forever [options]`

## Confiugration:
-----------------
The `config.py` file in the display directory/module is used by the web UI and command line utility. The below configurations are available:
 - `HOSTS` - A list of dictionaries that contain 2 keys: 1) `"hostname"` - the host name of the pi and 2) `"local_ip"` - the local IP address of the pi
 - `SERVICES` - A list of services (names of proccesses) to display in the services panel
 - `COUNT_DISPLAY_SERVICES` - A list of names from `SERVICES` that will display the number of running processes instead of `Running`/`Stopped`
 - `WIDTH` - Character width of each panel (height is automatically adjusted)
 - `VALUE_SPACING` - Character position of the status values in each panel
 - `API_PORT` - The web API port that will be used on each pi
 - `PCT_RED_THRESH` - The threshold used to color numeric values as red
 - `SLEEP_TIME` - The time to sleep between each refresh (when using `-r`/`--run-forever` in the terminal)
 - `TEMP_UNITS` - Units that the CPU temperature will be displayed in (fahrenheit/celsius)


## Examples:
-----------
#### Command:

`$ ./display.sh` or `$ python3 -m display`

NOTE: You can pass `--no-color` to not include coloring in the terminal display

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

<pre style="font-size:12.5">
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
