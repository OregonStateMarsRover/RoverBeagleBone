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
    def __init__(self, bus, roverStatusMutex, queueMutex, queue, RoverStatus):
        # Initializes threading
        threading.Thread.__init__(self)
        # Stores the bus and queue objects
        self.bus = bus
        self.queue = queue
        self.roverStatus = RoverStatus
        self.roverTimeout = 2  # Seconds to wait before killing the rover
        # Save Mutex's
        self.roverStatusMutex = roverStatusMutex
        self.queueMutex = queueMutex

    def run(self):
        print "Running Listener"
        intervalAlive_start = time.time()  # Start timer to catch roverAlive messages
        while 1:
            packet = None
            if (time.time() - intervalAlive_start) > self.roverTimeout:
                with self.roverStatusMutex:
                    self.roverStatus.roverAlive = 0
                print "LOST ROVER SIGNAL!!!"
                intervalAlive_start = time.time()  # Reset roverAlive timer
            if self.bus.base.inWaiting() > 0:
                packet = RoverPacket.from_rx(self.bus.base)  # Retreive bytearray
                #print packet
                if RoverPacket.checksum_error == 1:
                    bus.base.flushInput()
                    print "Flushed Base Input Buffer"
                    RoverPacket.checksum_error = 0
                    with self.roverStatusMutex:
                        self.roverStatus.checksum_errors += 1
                    continue
                if RoverPacket.unexpectedcontrolchar_error == 1:
                    bus.base.flushInput()
                    print "Flushed Base Input Buffer"
                    RoverPacket.unexpectedcontrolchar_error = 0
                    with self.roverStatusMutex:
                        self.roverStatus.unexpectedcontrolchar_errors += 1
                    continue
                if RoverPacket.start_byte_error == 1:
                    bus.base.flushInput()
                    print "Flushed Base Input Buffer"
                    RoverPacket.start_byte_error = 0
                    with self.roverStatusMutex:
                        self.roverStatus.start_byte_errors += 1
                    continue
                with self.roverStatusMutex:
                    if packet.addr == 1:
                        # BeagleBone
                        if packet.content[0] == 17:
                            self.roverStatus.roverAlive = 1
                            with self.queueMutex:
                                self.queue.put(['beaglebone'])
                            intervalAlive_start = time.time()  # Reset roverAlive timer
                    elif (packet.addr >= 2) and (packet.addr <= 7):
                        # Drive
                        self.roverStatus.wheel_commands[packet.addr - 2]['velo'] = packet.content[0]
                        self.roverStatus.wheel_commands[packet.addr - 2]['angle'] = packet.content[1]
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

    def emergencyStop(self):
        wheel = [2, 3, 4, 5, 6, 7]
        for wheelAddr in wheels:
            packet = BogiePacket(wheelAddr, 0, 0)
            with self.queueMutex:
                self.queue.put(packet)
