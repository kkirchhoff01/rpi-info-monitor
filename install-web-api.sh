#!/bin/bash

# LIB_INSTALLED=$((python3 -c "import rpimonitor" &> /dev/null ) ; echo $? )
LIB_INSTALLED=$(python3 -m pip freeze | grep rpimonitor | wc -l)

mkdir /usr/local/sbin/rpi-info-monitor
cp -r ./webdisplay /usr/local/sbin/rpi-info-monitor/
cp rpi-info-webapi.service /lib/systemd/system/

if [ $LIB_INSTALLED -eq 0 ]
then
    cp -r ./rpimonitor /usr/local/sbin/rpi-info-monitor/
fi

systemctl enable rpi-info-webapi.service
systemctl start rpi-info-webapi.service
