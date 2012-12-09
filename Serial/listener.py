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
		list = []
		while 1:
			if self.bus.base.inWaiting() > 0:
				packet = RoverPacket.from_rx(self.bus.base)	# Retreive bytearray
				#packet = self.bytearray_to_list(packet)		# Turn byte array into python list
				list.append(packet)
			elif (self.bus.base.inWaiting() == 0) and (list != []):
				self.queue.put(list)
				list = []

	def bytearray_to_list(self, data):
		# Takes in a bytearray in the form bytearray(b'\xca\x03\x03-\\\x04\xa2')
		# Return data from packet in the form [3, 0, 0] or [<addr>, <data>, <data>]
		packet_list = []
		for item in data:
			packet_list.append(item)
		# packet_list now looks similar to [202, 3, 4, 92, 4, 92, 4]
		return packet_list
	