########## Listener ##########

# Original Author: John Zeller

# The Listener, listens to all bus lines for any incoming packets. When a packet comes
# the listener grabs it and stores it into the queue for the receptionist

import sys
sys.path.append('/home/ubuntu/Serial')
import serial, time
import Queue
import threading
from roverpacket import *
from bus import *

class Listener(threading.Thread):
        def __init__(self, bus, queue):
                print "[%.4f] Initializing Thread in Listener" % time.clock()
                threading.Thread.__init__(self)
                print "[%.4f] Initializing Listener" % time.clock()
                self.bus = bus
                self.queue = queue

        def run(self):
                list = []
                print "[%.4f] Starting Listener" % time.clock()
                while 1:
                        if self.bus.base.inWaiting() > 0:
                                list.append(self.bus.base.read(1))
                        elif (self.bus.base.inWaiting() == 0) and (list != []):
                                self.queue.put(list)
                                list = []
