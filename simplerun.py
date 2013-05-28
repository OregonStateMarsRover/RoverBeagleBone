########## Simple Run - simplerun.py ##########

# Original Author: John Zeller

# The Listener, listens to the base station bus for any incoming packets.
# When a packet comes the listener grabs it, uses roverPacket to open it,
# and then stores the correct state values in roverStatus.

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

class SimpleRun(threading.Thread):
    def __init__(self, commands_queue):
        # Initializes threading
        threading.Thread.__init__(self)
        # Stores the bus
        self.queue = commands_queue
        self.bus = Bus()

    def run(self):
        while 1:
            packet = None
            if self.bus.base.inWaiting() > 0:
                if self.bus.base.inWaiting() > 1000:
                    self.bus.base.flushInput()
                    self.bus.base.flushOutput()
                packet = RoverPacket.from_rx(self.bus.base)  # Retreive bytearray
                packet = packet.msg()
                print self.bus.base.inWaiting()
                self.send_drive(packet)

    def send_drive(self, packet):
        self.queue.put(packet)


class Receptionist(object):
    def __init__(self):
        # Create Mutex's
        self.roverStatusMutex = Lock()
        self.queueMutex = Lock()

        self.bus = Bus()
        self.commands_queue = Queue.Queue()
        self.simplerun = SimpleRun(self.commands_queue)
        self.simplerun.start()


    def start(self):
        print "Starting Receptionist"
        # Flush ALL buffers before doing anything
        self.flush_all_buffers()
        self.flush_all_buffers()
        self.flush_all_buffers()
        self.flush_all_buffers()
        while 1:
            if self.commands_queue.empty() is False:
                packet = self.commands_queue.get()
                self.onrover_send_data(packet)


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