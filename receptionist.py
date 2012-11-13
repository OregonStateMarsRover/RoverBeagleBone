########## Receptionist ########## 

# Original Author: John Zeller

import sys
sys.path.append('/home/ubuntu/Serial')
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
                print "[%.4f] Creating Bus Object" % time.clock()
                self.bus = Bus()
                print "[%.4f] ..............%s" % (time.clock(), self.bus)
                # Create queue object which holds all packets waiting to be used
                print "[%.4f] Creating Queue Object" % time.clock()
                self.queue = Queue.Queue()
                print "[%.4f] ..............%s" % (time.clock(), self.queue)
                # Create listener object which will be launched on another thread
                # This listener, listens to every port and adds messages to the queue
                print "[%.4f] Creating Listener Thread Object" % time.clock()
                self.listenerthread = Listener(self.bus, self.queue)
                print "[%.5f] Starting Listener Thread" % time.clock()
                self.listenerthread.start()
                print "[%.5f] ..............THREAD STARTED!" % time.clock()

        def start(self):
                count = 0
                print "[%.4f] ..............Success!" % time.clock()
                while 1:
                        if count > 3:
                                print self.queue
                                count = 0
                        if self.queue.empty() is True:
                                print "Nothing to report!"
                                time.sleep(2)
                        else:
                                print self.queue.get()
                        count += 1
                        print "Woha!"


if __name__ == '__main__':
        receptionist = Receptionist()
        print "[%.4f] Starting Receptionist" % time.clock()
        receptionist.start()
