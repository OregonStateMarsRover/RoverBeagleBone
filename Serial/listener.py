########## Listener - listener.py ##########

# Original Author: John Zeller

# The Listener, listens to the base station bus for any incoming packets.
# When a packet comes the listener grabs it, uses roverPacket to open it,
# and then stores the correct state values in roverStatus.

import sys
sys.path.append('/home/ubuntu/RoverBeagleBone/Serial')
import serial
import time
import Queue
import threading
from threading import Lock
import time
from roverpacket import *
from bus import *

class Listener(threading.Thread):
    def __init__(self, bus, queue, roverStatus):
        # Initializes threading
        threading.Thread.__init__(self)
        # Stores the bus and queue objects
        self.bus = bus
        self.queue = queue
        self.roverStatus = roverStatus

    def run(self):
        while 1:
            packet = None
            if self.bus.base.inWaiting() > 0:
                if self.bus.base.inWaiting() > 1000:
                    self.bus.base.flushInput()
                    self.bus.base.flushOutput()
                try:
                    packet = RoverPacket.from_rx(self.bus.base)  # Retreive bytearray
                except:
                    continue
                if packet.addr == 1:
                    # BeagleBone
                    pass
                elif (packet.addr >= 2) and (packet.addr <= 7):
                    # Drive
                    self.roverStatus.wheel_commands[packet.addr - 2]['velo'] = packet.content[0]
                elif packet.addr == 8:
                    # Arm
                    secAddr = packet.content[0]
                    if secAddr == 1:
                        # Shoulder
                        arm_shoulder = packet.content[1] + packet.content[2]
                        self.roverStatus.arm_shoulder = arm_shoulder
                    elif secAddr == 2:
                        # Elbow
                        arm_elbow = packet.content[1] + packet.content[2]
                        self.roverStatus.arm_elbow = arm_elbow
                elif packet.addr == 9:
                    # Wrist
                    secAddr = packet.content[0]
                    if secAddr == 1:
                        # Angle
                        wrist_angle = packet.content[1] + packet.content[2]
                        self.roverStatus.wrist_angle = wrist_angle
                    elif secAddr == 2:
                        # Tilt
                        wrist_tilt = packet.content[1]
                        self.roverStatus.wrist_tilt = wrist_tilt
                    elif secAddr == 3:
                        # Scoop Actuate
                        scoop_toggle = packet.content[1]
                        if scoop_toggle == 1:
                            self.roverStatus.scoop_toggle = True
                        elif scoop_toggle == 0:
                            self.roverStatus.scoop_toggle = False
                    elif secAddr == 4:
                        # Probe Actuate
                        probe_distance = packet.content[1]
                        self.roverStatus.probe_distance = probe_distance
                    elif secAddr == 5:
                        # Probe Get Data
                        probe_toggle = packet.content[1]
                        if probe_toggle == 1:
                            self.roverStatus.probe_toggle = True
                        elif probe_toggle == 0:
                            self.roverStatus.probe_toggle = False
                    elif secAddr == 6:
                        # Get Voltage
                        voltage_toggle = packet.content[1]
                        if voltage_toggle == 1:
                            self.roverStatus.voltage_toggle = True
                        elif voltage_toggle == 0:
                            self.roverStatus.voltage_toggle = False
                elif packet.addr == 10:
                    # Tripod
                    secAddr = packet.content[0]
                    if secAddr == 1:
                        # Horizontal Servo
                        tri_hori = packet.content[1]
                        self.roverStatus.tri_hori = tri_hori
                    elif secAddr == 2:
                        # Vertical Servo
                        tri_vert = packet.content[1]
                        self.roverStatus.tri_vert = tri_vert
                    elif secAddr == 3:
                        # Zoom
                        tri_zoom = packet.content[1]
                        self.roverStatus.tri_zoom = tri_zoom
                elif packet.addr == 11:
                    # MUX
                    self.roverStatus.mux_cam = packet.content[0]
                elif packet.addr == 12:
                    # Package
                    package_select = packet.content[0]
                    if package_select == 1:
                        self.roverStatus.package_one = True
                    elif package_select == 2:
                        self.roverStatus.package_two = True
                    elif package_select == 3:
                        self.roverStatus.package_three = True
                    elif package_select == 4:
                        self.roverStatus.package_four = True
                    elif package_select == 5:
                        self.roverStatus.package_five = True
            #self.readGPS()

    def readGPS(self):
        gprmc_id = 'GPRMC'

        while 1:
            if self.bus.gps.inWaiting() > 0:
                byte = self.bus.gps.read(1)
                if byte == '$':
                    id = self.bus.gps.read(5)
                    if id == 'GPRMC':
                        msg = ''
                        while 1:
                            next = self.bus.gps.read(1)
                            if next == '$':
                                break
                            msg += next
                        msg = msg.split(',')

                        # Split into variables
                        utc_time = msg[1]
                        nav_rec_warn = msg[2]
                        latitude = msg[3] + msg[4]
                        longitude = msg[5] + msg[6]
                        speed = msg[7]
                        magnetic_variation = msg[10]

                        # Update Rover Status
#                        with self.roverStatus.roverStatusMutex:
                        self.roverStatus.utc_time = utc_time
                        self.roverStatus.latitude = latitude
                        self.roverStatus.longitude = longitude
                        self.roverStatus.speed_gps = speed
                        self.roverStatus.nav_rec_warn = nav_rec_warn
                        self.roverStatus.magnetic_var = magnetic_variation