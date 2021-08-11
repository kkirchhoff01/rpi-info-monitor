#!/bin/bash

cp -r ./rpimonitorapi /usr/local/sbin/
cp rpi-info-api.service /lib/systemd/system/
systemctl enable rpi-info-api.service
systemctl start rpi-info-api.service
