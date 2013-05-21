# bogietest.py 
# Mike Fortner
# Script for testing communication with the bogie controllers
# Use on the command line to generate packets over the serial port 

import sys
import serial
import time

if __name__ == '__main__':
        bus = serial.Serial(port='/dev/ttyO2',
                                baudrate=38400)
	bus.flushInput()
	bus.flushOutput()

	gprmc_id = 'GPRMC'

	while 1:
		if bus.inWaiting() > 0:
			byte = bus.read(1)
			if byte == '$':
				id = bus.read(5)
				if id == 'GPRMC':
					msg = ''
					while 1:
						next = bus.read(1)
						if next == '$':
							break
						msg += next
					msg = msg.split(',')

					# Split into variables
					utc_time = msg[1]
					nav_rec_warn = msg[2]
					latitude = msg[3] + msg[4]
					longitude = msg[5] + msg[6]
					speed = msg[7]
					course_made_good = msg[8]
					date = msg[9]
					magnetic_variation = msg[10]
					checksum = msg[11][0:4]

					# Decode variables
					utc_time = utc_time[0:2] + ":" + utc_time[2:4] + ":" + utc_time[4:6] + " UTC"
					if nav_rec_warn == "V":
						nav_rec_warn = "Warning!"
					elif nav_rec_warn == "A":
						nav_rec_warn = "OK!"
					date = date[2:4] + "/" + date[0:2] + "/" + date[4:6]

					print "UTC Time: ", utc_time
					print "Nav Rec Warning: ", nav_rec_warn
					print "Latitude: ", latitude
					print "Longitude: ", longitude
					print "Speed: ", speed
					print "Course Made Good: ", course_made_good
					print "Date of Fix: ", date
					print "Magnetic Variation: ", magnetic_variation
					print "Checksum: ", checksum
					print "\n"
