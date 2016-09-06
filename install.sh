#!/bin/bash

#This script makes the program autorun on startup, and This script must be
#run with sudo.

#check if run with sudo
if (( $EUID != 0 )); then
    echo "Error: install must be run as root."
    exit
fi


#download and install Adafruit's Python DHT Library
mkdir /tmp/rpi-fan-controller
wget -O /tmp/rpi-fan-controller/master.zip https://github.com/adafruit/Adafruit_Python_DHT/archive/master.zip
unzip /tmp/rpi-fan-controller/master.zip -d /tmp/rpi-fan-controller/
python /tmp/rpi-fan-controller/Adafruit_Python_DHT-master/setup.py install

#make sure the file doesn't already exist
if [ -e /lib/systemd/system/piFans.service ]; then
    echo "Error: Service piFans already exists. Cannot create autorun service."
    echo "File /lib/systemd/system/piFans.service already exists."
    exit
fi

#go ahead and install

#copy the autorun file to a service
cp autorun.txt /lib/systemd/system/piFans.service
#change the mode of the service
chmod 644 /lib/systemd/system/piFans.service
#reload the daemon
systemctl daemon-reload
#enable the service
systemctl enable piFans.service
#start the service
systemctl start piFans.service
