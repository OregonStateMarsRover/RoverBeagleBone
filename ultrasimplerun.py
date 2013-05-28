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
from bus import *

class SimpleRun(object):
    def __init__(self):
        self.bus = Bus()

    def run(self):
        while 1:
            packet = None
            if self.bus.base.inWaiting() > 0:
                byte = self.bus.base.read(1)
                self.bus.drive.write(byte)

if __name__ == '__main__':
    simplerun = SimpleRun()
    simplerun.run()