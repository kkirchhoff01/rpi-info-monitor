#!/bin/bash

if ! command -v python3 &> /dev/null
then
    apt-get install python3 python3-pip
fi

$(which python3) -m pip install -r requirements.txt

cp -r ./rpimonitorapi /usr/local/sbin/
cp rpi-info-api.service /lib/systemd/system/
systemctl enable rpi-info-api.service
systemctl start rpi-info-api.service
