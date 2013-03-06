########## Receptionist ##########

# Original Author: John Zeller

# The Receptionist watches a queue of packets and executes the packets in FIFO ordering.
# The Listener is launched in a separate thread to bring in messages from outside the
# BeagleBone and adds them to the queue for the Receptionist to then execute.

import sys
sys.path.append('/home/ubuntu/RoverBeagleBone/Serial')
sys.path.append('/home/ubuntu/RoverBeagleBone/core')
import serial
import time
import Queue
import threading
from roverpacket import *
from bus import *
from listener import *
from queuer import *
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
        self.commands_queue = Queue.Queue()
        self.roverStatus = RoverStatus
        # This listener, listens to every port and adds messages to the queue
        self.listenerthread = Listener(self.bus, self.commands_queue, RoverStatus)
        self.listenerthread.start()
        # The Queuer, reads roverStatus for commands, then assembles packets for receptionist to send
        # to all of the modules based on those commands
        self.queuerthread = Queuer(self.commands_queue, RoverStatus)
        self.queuerthread.start()

    def start(self):
        print "Starting Receptionist"
        while 1:
            if self.commands_queue.empty() is False:
                packet = self.commands_queue.get()
                self.onrover_send_data(packet)

            # if self.rover_queue.empty() is False:
            #	# Do Something

    def onrover_send_data(self, packet):
        # This function receives a packet and determines where to
        # send it and then sends it
        if packet[0] == 'beaglebone':
            self.bbcount = self.bbcount + 1
            print "BeagleBone packet %d received!" % self.bbcount
        if packet[0] == 'drive':
            self.drivecount = self.drivecount + 1
            print "Drive packet ", self.drivecount, " received! - Address: ", packet[1], \
                "Speed: ", self.roverStatus.wheel_commands[packet[1] - 2]['velo'], \
                " Angle: ", self.roverStatus.wheel_commands[packet[1] - 2]['angle']
        elif packet[0] == 'arm':
            self.armcount = self.armcount + 1
            print "Arm packet %d received!" % self.armcount
            self.bus.arm.write(packet[2])
        elif packet[0] == 'tripod':
            self.tripodcount = self.tripodcount + 1
            print "Tripod packet %d received!" % self.tripodcount
            self.bus.tripod.write(packet[2])
        elif packet[0] == 'mux':
            self.muxcount = self.muxcount + 1
            print "MUX packet %d received!" % self.muxcount
#			self.bus.mux.write(packet[2])
        elif packet[0] == 'package':
            self.packagecount = self.packagecount + 1
            print "Package packet %d received!" % self.packagecount
#			self.bus.package.write(packet[2])

if __name__ == '__main__':
    receptionist = Receptionist()
    receptionist.start()
