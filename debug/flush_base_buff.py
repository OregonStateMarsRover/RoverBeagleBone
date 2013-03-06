import sys
sys.path.append('/home/ubuntu/RoverBeagleBone/Serial')
import serial, time
from bus import *

bus = Bus()
bus.base.flushInput()
print "Flushed Base Input Buffer"
bus.drive.flushOutput()
print "Flushed Rover Output Buffer"
