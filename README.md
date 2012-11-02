RoverBeagleBone
===============


When pulling the repo to the BeagleBone, there is a set of things that
must occur before a new BeagleBone will function properly.
Detailed instructions can be found in the README.txt file in this repo

## Initializations
### 1. Update the OS on the BeagleBone to Ubuntu 12.04
### 2) Once in the BeagleBone, you'll need to 'install' the init.d scripts in the /InitScripts directory, by using the following commands:
    rm /etc/network/interfaces
    cp /home/ubuntu/RoverBeagleBone/InitScripts/interfaces /etc/network
    cp /home/ubuntu/RoverBeagleBone/InitScripts/initdhclient.sh /etc/init.d
    chmod +x /etc/init.d/initdhclient.sh
    update-rc.d dhclientinit.sh defaults
    cp /home/ubuntu/RoverBeagleBone/InitScripts/inituart.sh /etc/init.d
    chmod +x /etc/init.d/inituart.sh
    update-rc.d inituart.sh defaults

## General
### 1) 
