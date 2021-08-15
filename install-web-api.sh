#!/bin/bash

mkdir /usr/local/sbin/rpi-info-monitor
cp -r ./webdisplay /usr/local/sbin/rpi-info-monitor/
cp -r ./display /usr/local/sbin/rpi-info-monitor/
cp rpi-info-webapi.service /lib/systemd/system/
systemctl enable rpi-info-webapi.service
systemctl start rpi-info-webapi.service
