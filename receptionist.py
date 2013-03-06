########## Receptionist ########## 

# Original Author: John Zeller

# The Receptionist watches a queue of packets and executes the packets in FIFO ordering.
# The Listener is launched in a separate thread to bring in messages from outside the
# BeagleBone and adds them to the queue for the Receptionist to then execute.

import sys
sys.path.append('/home/ubuntu/RoverBeagleBone/Serial')
sys.path.append('/home/ubuntu/RoverBeagleBone/core')
import serial, time
import Queue
import threading
from roverpacket import *
from bus import *
from listener import *
from rover_status import *

class Receptionist(object):
	def __init__(self):
		self.drivecount = 0
		self.bbcount = 0
		self.armcount = 0
		self.tripodcount = 0
		self.muxcount = 0
		self.packagecount = 0
		self.bus = Bus()
		self.base_queue = Queue.Queue()
		# This listener, listens to every port and adds messages to the queue
		self.listenerthread = Listener(self.bus, self.base_queue, RoverStatus)
		self.listenerthread.start()

	def start(self):
		print "Starting Receptionist"
		while 1:
			if self.base_queue.empty() is False:
				packet = self.base_queue.get()
				self.onrover_send_data(packet)

			#if self.rover_queue.empty() is False:
			#	# Do Something
		
	def onrover_send_data(self, packet):
		# This function receives a packet and determines where to
		# send it and then sends it
		if packet[0] == 'beaglebone':
			self.bbcount = self.bbcount + 1
			print "BeagleBone packet %d received!" % self.bbcount
		if packet[0] == 'drive':
			self.count = self.drivecount + 1
			print "Drive packet %d received!" % self.drivecount
		elif packet[0] == 'arm':
			self.count = self.armcount + 1
			print "Arm packet %d received!" % self.armcount
			self.bus.arm.write(packet[1])
		elif packet[0] == 'tripod':
			self.count = self.tripodcount + 1
			print "Tripod packet %d received!" % self.tripodcount
			self.bus.tripod.write(packet[1])
		elif packet[0] == 'mux':
			self.count = self.muxcount + 1
			print "MUX packet %d received!" % self.muxcount
#			self.bus.mux.write(packet[1])
		elif packet[0] == 'package':
			self.count = self.packagecount + 1
			print "Package packet %d received!" % self.packagecount
#			self.bus.package.write(packet[1])

if __name__ == '__main__':
	receptionist = Receptionist()
	receptionist.start()

