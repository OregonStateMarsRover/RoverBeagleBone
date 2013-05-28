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
        # Create Mutex's
#        self.roverStatusMutex = Lock()
#        self.queueMutex = Lock()

        self.bus = Bus()
        self.commands_queue = Queue.Queue()
        self.roverStatus = RoverStatus()#self.roverStatusMutex, self.queueMutex)
        # This listener, listens to every port and adds messages to the queue
        self.listenerthread = Listener(self.bus, self.commands_queue, self.roverStatus)
        self.listenerthread.start()
        # The Queuer, reads roverStatus for commands, then assembles packets for receptionist to send
        # to all of the modules based on those commands
        self.queuerthread = Queuer(self.commands_queue, self.roverStatus)
        self.queuerthread.start()


    def start(self):
        print "Starting Receptionist"
        # Flush ALL buffers before doing anything
        self.flush_all_buffers()
        self.flush_all_buffers()
        self.flush_all_buffers()
        self.flush_all_buffers()
        while 1:
            if self.commands_queue.empty() is False:
#                with self.roverStatus.queueMutex:
                packet = self.commands_queue.get()
                self.onrover_send_data(packet)

    def onrover_send_data(self, packet):
        # This function receives a packet and determines where to
        # send it and then sends it
        if packet[0] == 'beaglebone':
            pass
        if packet[0] == 'drive':
            pck = packet[1]
            self.bus.drive.write(pck)
            print self.bus.base.inWaiting()
            #print "Drive:", repr(pck)
        elif packet[0] == 'arm':
            pck = packet[1]
            self.bus.arm.write(pck)
        elif packet[0] == 'tripod':
            pck = packet[1]
            self.bus.tripod.write(pck)
        elif packet[0] == 'package':
            print "Package!"
        elif packet[0] == 'stillcamera':
            print "Still Camera!"

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
