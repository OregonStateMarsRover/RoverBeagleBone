# bogietest.py 
# Mike Fortner
# Script for testing communication with the bogie controllers
# Use on the command line to generate packets over the serial port 

import sys
import serial

if __name__ == '__main__':
#        usb0 = serial.Serial(port='/dev/ttyUSB0',
#                                baudrate=115200)
#        usb1 = serial.Serial(port='/dev/ttyUSB1',
#                                baudrate=115200)
	bus0 = serial.Serial(port='/dev/ttyO0',
				baudrate=115200)
        bus1 = serial.Serial(port='/dev/ttyO1',
                                baudrate=115200)
        bus2 = serial.Serial(port='/dev/ttyO2',
                                baudrate=115200)
        bus4 = serial.Serial(port='/dev/ttyO4',
                                baudrate=115200)
        bus5 = serial.Serial(port='/dev/ttyO5',
                                baudrate=115200)

	while 1:
#                if usb0.inWaiting() > 0:
#                        print "ttyUSB0: ", usb0.read(1)
#                if usb1.inWaiting() > 0:
#                        print "ttyUSB1: ", usb1.read(1)
		if bus0.inWaiting() > 0:
			print "ttyO0: ", bus0.read(1)
                if bus1.inWaiting() > 0:
                        print "ttyO1: ", bus1.read(1)
                if bus2.inWaiting() > 0:
                        print "ttyO2: ", bus2.read(1)
                if bus4.inWaiting() > 0:
                        print "ttyO4: ", bus4.read(1)
                if bus5.inWaiting() > 0:
                        print "ttyO5: ", bus5.read(1)

