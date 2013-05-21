# bogietest.py 
# Mike Fortner
# Script for testing communication with the bogie controllers
# Use on the command line to generate packets over the serial port 

import sys
import serial
import time

if __name__ == '__main__':
        bus2 = serial.Serial(port='/dev/ttyO2',
                                baudrate=9600)
	bus2.flushInput()
	bus2.flushOutput()

	sat_id = '/x72'
	empty = ''

	while 1:
		if bus2.inWaiting() > 0:
			byte = bus2.read(1)
			#byte = repr(byte)[3:5]
			#byte = int(byte, 16)
			#byte = str(unichr(byte))
			if byte == '\x10':
				print "Start"
				id = bus2.read(1)
				print "ID: ", repr(id)
				length = bus2.read(1)
				if length != empty:
					try:
						length = repr(length)[3:5]
						length = int(length, 16) # Read length and convert to int
						print "Length: ", length
					except:
						continue
				else:
					print "Length: BLANK"
				#msg = bus2.read(length)
				#print repr(msg)
			#print repr(byte).decode("hex")
	
