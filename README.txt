RoverBeagleBone
===============


When pulling the repo to the BeagleBone, there is a set of things that
must occur before a new BeagleBone will function properly.

Initializations
1) Update the OS on the BeagleBone to Ubuntu 12.04
	a) Remove the SD card from BeagleBone and format it.
	b) Download the most recent copy of the 12.04 Ubuntu distro 
	   specifically built for BeagleBone. Most recent .tar.xz files 
	   can be found here:
		http://rcn-ee.net/deb/rootfs/precise/
	c) Once you have downloaded the .tar.xz file, navigate to the 
	   directory that the file is in and unpack it using the following 
	   commands:
		tar -xJf [file_name].tar.xz
	d) The file is now unpacked, cd into the new directory
	e) Find the location of your sd card using:
		sudo ./setup_sdcard.sh --probe-mmc
	f) Now push the image to your sd card using:
		sudo ./setup_sdcard.sh --mmc /dev/mmcblk0 --uboot "bone"
	g) Now replace the sd card and power on the BeagleBone, and login:
		Username: ubuntu
		Password: temppwd
	   NOTE: Directions follow this tutorial:
		http://fleshandmachines.wordpress.com/2012/05/03/beaglebone-on-ubuntu-11-04/
2) Once in the BeagleBone, you'll need to 'install' the init.d scripts in the
   /InitScripts directory, by using the following commands:
	rm /etc/network/interfaces
	cp /home/ubuntu/RoverBeagleBone/InitScripts/interfaces /etc/network
	cp /home/ubuntu/RoverBeagleBone/InitScripts/initdhclient.sh /etc/init.d
	chmod +x /etc/init.d/initdhclient.sh
	update-rc.d dhclientinit.sh defaults
	cp /home/ubuntu/RoverBeagleBone/InitScripts/inituart.sh /etc/init.d
	chmod +x /etc/init.d/inituart.sh
	update-rc.d inituart.sh defaults
	cp /home/ubuntu/RoverBeagleBone/InitScripts/initip.sh /etc/init.d
	chmod +x /etc/init.d/initip.sh
	update-rc.d initip.sh defaults
	cp /home/ubuntu/RoverBeagleBone/start.sh /etc/init.d
	chmod +x /etc/init.d/start.sh
	update-rc.d start.sh defaults
	
	NOTE: This initialization sets up the eth0 for SSH and the UART
	      configurations.
3) Transfer and install the pySerial library to the BeagleBone:
	a) Download pySerial on your laptop here: 
		http://pypi.python.org/packages/source/p/pyserial/pyserial-2.6.tar.gz
	b) Follow the instructions in General #2 to transfer pyserial-2.6.tar.gz to the BeagleBone
	c) Once on the BeagleBone, expand the .tar.gz file
	d) cd into the newly expanded directory pyserial-2.6 and type:
		sudo python setup.py install
	e) You have installed pySerial!
4) Disable refreshing of /dev/ttyO0 on the BeagleBone to allow for using that port as a serial communication only port.
	a) Type, "nano /etc/init/serial.conf"
	b) Replace the line that says "exec /sbin/getty 115200 ttyO0" with "#exec /sbin/getty 115200 ttyO0"

## General
### 1) How to setup an SSH connection between your Ubuntu laptop and the BeagleBone
	a) Connect an Ethernet cable from the BeagleBone to your laptop.
	b) Click on the Internet icon in the upper righthand corner of your laptop screen, 
		then select 'Edit Connections', then 'Wired Connection 1', and then 'Edit'
	c) Select the 'IPv4 Settings' tab, and then change method to 'Manual'
	d) Add an address with the following values:
		Address: 10.0.0.2
		Netmask: 255.255.255.0
		Gateway: 10.0.0.1
	   Now 'Save'
	   NOTE: What this does is set the laptop to be 10.0.0.2 and 
		 then the BeagleBone to be 10.0.0.1
	e) Now that the laptop is configured, go to the BeagleBone and type:
		sudo ifconfig 10.0.0.1
	   NOTE: Before, we setup the laptop, but the BeagleBone did not
		 know it's own address. This sets up its address.
	f) Now, from the BeagleBone type:
		ping 10.0.0.2
	g) You should see it succeed. Now, from the laptop type:
		ping 10.0.0.1
	h) You should see it succeed. Now, from the laptop type:
		sudo ssh ubuntu@10.0.0.1
		Type your password
	i) You are now connected via SSH!
### 2) If BeagleBone is not attached to an internet connection, but just through SSH, you can 
	transfer files like this:
		scp file_name ubuntu@10.0.0.1:/home/ubuntu/
	a) Additionally if you need to transfer whole files, you can just make it a tar.gz
		tar cvzf tarfile.tar.gz files...
	   To expand .tar.gz
		tar xzvf tarfile.tar.gz
### 3) 

