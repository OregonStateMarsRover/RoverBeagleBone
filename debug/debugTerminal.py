import sys
sys.path.append('/home/ubuntu/RoverBeagleBone/Serial')
import serial, time
from bus import *
from roverpacket import *

bus = Bus()
while 1:
	print bus.base.inWaiting()
#		if bus.base.inWaiting() > 0:
#			#packet = self.unpack_packet()
#			packet = RoverPacket.from_rx(self.bus.base)	# Retreive bytearray
#			print packet					# Print Raw Packet
#			packet = packet.msg()
#			self.queue.put(packet)
