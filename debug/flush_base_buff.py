import sys
sys.path.append('/home/ubuntu/RoverBeagleBone/Serial')
import serial, time
from bus import *

bus = Bus()
bus.base.flushInput()
print "Flushed Base Input Buffer"
bus.motor.flushOutput()
print "Flushed Rover Output Buffer"
