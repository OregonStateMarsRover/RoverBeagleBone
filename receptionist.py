########## Receptionist ##########

# Original Author: John Zeller

# The Receptionist watches a queue of packets and executes the packets in FIFO ordering.
# The Listener is launched in a separate thread to bring in messages from outside the
# BeagleBone and adds them to the queue for the Receptionist to then execute.

import sys
sys.path.append('/home/ubuntu/RoverBeagleBone/Serial')
sys.path.append('/home/ubuntu/RoverBeagleBone/core')
sys.path.append('/home/ubuntu/RoverBeagleBone/debug')
import serial
import time
import Queue
import threading
from threading import Lock
from roverpacket import *
from bus import *
from listener import *
from queuer import *
from rover_status import *
from debugTerminalStates import *


class Receptionist(object):
    def __init__(self):
        self.drivecount = 0
        self.bbcount = 0
        self.armcount = 0
        self.tripodcount = 0
        self.muxcount = 0
        self.packagecount = 0

        # Create Mutex's
        self.roverStatusMutex = Lock()
        self.queueMutex = Lock()

        self.bus = Bus()
        self.commands_queue = Queue.Queue()
        self.roverStatus = RoverStatus(self.roverStatusMutex, self.queueMutex)
        # This listener, listens to every port and adds messages to the queue
        self.listenerthread = Listener(self.bus, self.commands_queue, self.roverStatus)
        self.listenerthread.start()
        # The Queuer, reads roverStatus for commands, then assembles packets for receptionist to send
        # to all of the modules based on those commands
        self.queuerthread = Queuer(self.commands_queue, self.roverStatus)
        self.queuerthread.start()
        # The Debug Terminal States, reads roverStatus and displays the changing values on the Terminal
        # for debugging purposes
#        self.debugthread = debugTerminalStates(self.roverStatus)
#        self.debugthread.start()


    def start(self):
        print "Starting Receptionist"
        # Flush ALL buffers before doing anything
        self.flush_all_buffers()
        self.flush_all_buffers()
        self.flush_all_buffers()
        self.flush_all_buffers()
        while 1:
            print self.bus.base.inWaiting()
            if self.commands_queue.empty() is False:
                with self.roverStatus.queueMutex:
                    packet = self.commands_queue.get()
                #print packet
                self.onrover_send_data(packet)

            # if self.rover_queue.empty() is False:
            #	# Do Something

    def onrover_send_data(self, packet):
        # This function receives a packet and determines where to
        # send it and then sends it
        if packet[0] == 'beaglebone':
            self.bbcount = self.bbcount + 1
            #print "BeagleBone packet %d received!" % self.bbcount
        if packet[0] == 'drive':
            self.drivecount = self.drivecount + 1
            addr = packet[1]
            pck = packet[2]
            self.bus.drive.write(pck)
	    #print "Drive", self.drivecount, "-", addr, velo, angle
        elif packet[0] == 'arm':
            self.armcount = self.armcount + 1
            pck = packet[2]
            self.bus.arm.write(pck)
            #print "Arm %d" % self.armcount
            self.bus.arm.write(packet[2])
        elif packet[0] == 'tripod':
            self.tripodcount = self.tripodcount + 1
            #print "Tripod %d" % self.tripodcount
            self.bus.tripod.write(packet[2])
        elif packet[0] == 'mux':
            self.muxcount = self.muxcount + 1
            #print "MUX %d" % self.muxcount
#			self.bus.mux.write(packet[2])
        elif packet[0] == 'package':
            self.packagecount = self.packagecount + 1
            #print "Package %d" % self.packagecount
#			self.bus.package.write(packet[2])

    def flush_all_buffers(self):
        self.bus.base.flushInput()
        self.bus.base.flushOutput()
        self.bus.arm.flushInput()
        self.bus.arm.flushOutput()
        self.bus.tripod.flushInput()
        self.bus.tripod.flushOutput()
        self.bus.drive.flushInput()
        self.bus.drive.flushOutput()

if __name__ == '__main__':
    receptionist = Receptionist()
    receptionist.start()
