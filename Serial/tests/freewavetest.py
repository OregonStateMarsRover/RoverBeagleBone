import sys
import serial
from roverpacket import *

if __name__ == '__main__':
        bus = serial.Serial(port='/dev/ttyO5',
                                baudrate=115200)

        while 1:
                if bus.inWaiting() > 0:
                    packet = RoverPacket.from_rx(bus)
                    print repr(packet)
#                        byte = bus.read(1)
#                        if byte == '\xca':
#                            print "\n", repr(byte)
#                        else:
#                            print repr(byte),