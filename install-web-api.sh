#!/bin/bash

WEB_PATH=$(pwd)

cp -r ./webdisplay /usr/local/sbin/rpiwebdisplay
cp rpi-info-webapi.service /lib/systemd/system/
sed -i -E "s|WEB_PATH|$WEB_PATH|g" /lib/systemd/system/rpi-info-webapi.service
systemctl enable rpi-info-webapi.service
systemctl start rpi-info-webapi.service
