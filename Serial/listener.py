########## Listener ##########

# Original Author: John Zeller

# The Listener, listens to all bus lines for any incoming packets. When a packet comes
# the listener grabs it and stores it into the queue for the receptionist

import sys
sys.path.append('/home/ubuntu/RoverBeagleBone/Serial')
import serial
import time
import Queue
import threading
import time
from roverpacket import *
from bus import *


class Listener(threading.Thread):
    def __init__(self, bus, queue, RoverStatus):
        # Initializes threading
        threading.Thread.__init__(self)
        # Stores the bus and queue objects
        self.bus = bus
        self.queue = queue
        self.roverStatus = RoverStatus

    def run(self):
        print "Running Listener"
        intervalAlive_start = time.time() # Start timer to catch roverAlive messages
        while 1:
		packet = None
        	if (time.time() - intervalAlive_start) > 4: # If it has been 4 seconds since hearing from the rover
        		self.roverStatus.roverAlive = 0
        		intervalAlive_start = time.time() # Reset roverAlive timer
            	if self.bus.base.inWaiting() > 0:
                	address = None
                	packet = RoverPacket.from_rx(self.bus.base)  # Retreive bytearray
	                if RoverPacket.checksum_error == 1:
	                    flushAll()
	                    RoverPacket.checksum_error = 0
	                    continue
	                if packet.addr == 1:
	                    address = 'beaglebone'
	                    if packet.content[0] == 17:
	                    	self.roverStatus.roverAlive = 1
	                    	intervalAlive_start = time.time() # Reset roverAlive timer
	                elif (packet.addr >= 2) and (packet.addr <= 7):
	                    address = 'drive'
	                    self.roverStatus.wheel_commands[packet.addr - 2]['velo'] = packet.content[0]
	                    self.roverStatus.wheel_commands[packet.addr - 2]['angle'] = packet.content[1]
	                elif packet.addr == 8:
	                    address = 'arm'
	                elif packet.addr == 9:
	                    address = 'tripod'
	                elif packet.addr == 10:
	                    address = 'mux'
	                elif packet.addr == 11:
	                    address = 'package'

    def flushAll(self):
        bus.base.flushInput()
        print "Flushed Base Input Buffer"

    def emergencyStop(self):
        wheel = [2, 3, 4, 5, 6, 7]
        for wheelAddr in wheels:
            packet = BogiePacket(wheelAddr, 0, 0)
            self.queue.put(packet)
