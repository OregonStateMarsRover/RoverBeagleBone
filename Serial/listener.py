########## Listener ##########

# Original Author: John Zeller

# The Listener, listens to all bus lines for any incoming packets. When a packet comes
# the listener grabs it and stores it into the queue for the receptionist

import sys
sys.path.append('/home/ubuntu/RoverBeagleBone/Serial')
import serial, time
import Queue
import threading
from roverpacket import *
from bus import *

class Listener(threading.Thread):
	def __init__(self, bus, queue):
		# Initializes threading
		threading.Thread.__init__(self)
		# Stores the bus and queue objects
		self.bus = bus
		self.queue = queue

	def run(self):
		print "Running Listener"
		while 1:
			if self.bus.base.inWaiting() > 0:
				packet = self.unpack_packet()
				self.queue.put(packet)

	def unpack_packet(self):
		temp = RoverPacket.from_rx(self.bus.base)	# Retreive bytearray
		packet = []
		packet.append(temp.addr)
		packet = packet + list(temp.content)
		return packet