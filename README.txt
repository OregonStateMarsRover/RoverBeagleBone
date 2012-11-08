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
	
	NOTE: This initialization sets up the eth0 for SSH and the UART
	      configurations.

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
### 2)