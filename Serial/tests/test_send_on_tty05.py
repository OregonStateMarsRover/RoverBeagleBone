# bogietest.py 
# Mike Fortner
# Script for testing communication with the bogie controllers
# Use on the command line to generate packets over the serial port 

import sys
import serial

if __name__ == '__main__':
	bus = serial.Serial(port='/dev/ttyO5',
				baudrate=115200)
	while 1:
		if bus.inWaiting() > 0:
			print bus.read(1)
