#!/bin/bash

if ! command -v python3 &> /dev/null
then
    apt-get install python3 python3-pip
fi

$(which python3) -m pip install -r requirements-webdisplay.txt

mkdir /usr/local/sbin/rpi-info-monitor
cp -r ./webdisplay /usr/local/sbin/rpi-info-monitor/
cp rpi-info-webapi.service /lib/systemd/system/

LIB_INSTALLED=$(python3 -c "import rpimonitor" &> /dev/null ; echo $? )

if [ $LIB_INSTALLED -ne 0 ]
then
    cp -r ./rpimonitor /usr/local/sbin/rpi-info-monitor/
fi

systemctl enable rpi-info-webapi.service
systemctl start rpi-info-webapi.service
