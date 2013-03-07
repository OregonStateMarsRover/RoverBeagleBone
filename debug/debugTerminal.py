import sys
sys.path.append('/home/ubuntu/RoverBeagleBone/Serial')
import serial, time
from bus import *
from roverpacket import *

bus = Bus()
while 1:
#	print bus.base.inWaiting()
		if bus.base.inWaiting() > 0:
			packet = RoverPacket.from_rx(bus.base)	# Retreive bytearray
			print packet					# Print Raw Packet
