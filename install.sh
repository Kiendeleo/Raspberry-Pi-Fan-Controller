#This script makes the program autorun on startup, and This script must be
#run with sudo.

#check if run with sudo
if (( $EUID != 0 )); then
    echo "Error: install must be run as root."
    exit
fi

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
