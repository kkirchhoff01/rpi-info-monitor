#!/bin/bash

mkdir /usr/local/sbin/rpi-monitor-api
cp -r ./rpimonitorapi /usr/local/sbin/rpi-monitor-api/
cp -r ./display /usr/local/sbin/rpi-monitor-api/
cp rpi-info-webapi.service /lib/systemd/system/
systemctl enable rpi-info-webapi.service
systemctl start rpi-info-webapi.service
