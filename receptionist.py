########## Receptionist ########## 

# Original Author: John Zeller

# The Receptionist watches a queue of packets and executes the packets in FIFO ordering.
# The Listener is launched in a separate thread to bring in messages from outside the
# BeagleBone and adds them to the queue for the Receptionist to then execute.

import sys
sys.path.append('/home/ubuntu/RoverBeagleBone/Serial')
import serial, time
import Queue
import threading
from roverpacket import *
from bus import *
from listener import *

# Initialization of interrupts



# Receptionist
class Receptionist(object):
	def __init__(self):
		# Create bus object which holds all initialized ports
		self.bus = Bus()
		# Create queue object which holds all packets waiting to be used
		self.queue = Queue.Queue()
		# Create listener object which will be launched on another thread
		# This listener, listens to every port and adds messages to the queue
		self.listenerthread = Listener(self.bus, self.queue)
		self.listenerthread.start()

	def start(self):
		print "Starting Receptionist"
		while 1:
<<<<<<< HEAD
			# Check the queue that holds things coming from base
			if self.queue.empty() is False:
				packet = self.queue.get()
				#print repr(packet)
				self.onrover_send_data(packet)
				self.bus.motor.write(packet)
			## Check the queue that holds things coming from rover
			#if self.roverqueue.empty() is False:
			#	# Do Something
		
	def onrover_send_data(self, packet):
		# This function receives a packet and determines based on its addresss
		# 	where to send it and then builds a packet in the correct format
		if packet[0] >= 2 and packet[0] <= 7:	# Then Bogie Address
			addr = packet[0]
			speed = packet[1]
			angle = packet[2]
			complete_packet = BogiePacket(addr, speed, angle)
			complete_packet = complete_packet.msg()
			# Hack Fix
			temp =  repr(complete_packet)
			temp_check = temp[-3]		# Grabs the checksum packet
			# Look at temp_check and determine its ASCII value
			# Convert its ASCII value to a hex value
			# Insert the hex value into place where checksum should be - ie temp[-3]
			#temp_char = ''	
			#temp[-3:] = temp_char
			self.bus.motor.write(complete_packet)
		#elif packet[0] >= 8 and packet[0] <= 9:	# Then Tripod Address
		#	# Do something
		#elif packet[0] >= 10 and packet[0] <= 13:# Then Arm Address
		#	# Do something
		#elif packet[0] == 14:	# Then GPS Address
		#	# Do something
		#elif packet[0] == 15:	# Then MUX Address
		#	# Do something
		#elif packet[0] == 16:	# Then Package Delivery Address
		#	# Do something
	
=======
			if self.queue.empty() is False:
				print self.queue.get()
>>>>>>> fa3056b604486f6713ad0d3c07ef9aafeff3653f
	

if __name__ == '__main__':
	receptionist = Receptionist()
	receptionist.start()

