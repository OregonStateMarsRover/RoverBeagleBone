########## Queuer - queuer.py ##########

# Original Author: John Zeller

# The Queuer looks at Rover_Status to determine, based on the values of the
# Joy, what address, speed and angle commands are necessary. It then adds
# these commands in the form of a tuple (addr, speed, angle) to the receptionist_queue

import time
import threading
from threading import Lock
from roverpacket import *
from bus import *

class Queuer(threading.Thread):
    def __init__(self, roverStatusMutex, queueMutex, receptionist_queue, roverStatus):
        threading.Thread.__init__(self)
        self.receptionist_queue = receptionist_queue
        self.roverStatus = roverStatus
        self.waitTime = 0.02  # Wait 20ms between packet cycles
        # Save Mutex's
        self.roverStatusMutex = roverStatusMutex
        self.queueMutex = queueMutex

    def run(self):
        while 1:
            with self.roverStatusMutex:
                roverAlive = self.roverStatus.roverAlive
            if roverAlive == 1:
                # Make Drive Commands
                drive_commands = self.poll_drive_command()
                drive_commands = self.assemble_drive_packet(drive_commands)
                for command in drive_commands:
                    command = ['drive', command[1], command]
                    with self.queueMutex:
                        self.receptionist_queue.put(command)
                # Make Arm Commands
                arm_commands = self.poll_drive_arm_command()
                arm_commands = self.assemble_arm_packets(arm_commands)
                for command in arm_commands:
                    command = ['arm', command[1], command]
                    with self.queueMutex:
                        self.receptionist_queue.put(command)
            elif roverAlive == 0:
                # Make Rover STOP Immediately - Connection has been lost
                drive_commands = self.assemble_stop_drive_packets()
                for command in drive_commands:
                    command = ['drive', command[1], command]
                    with self.queueMutex:
                        self.receptionist_queue.put(command)
            time.sleep(self.waitTime)

    def assemble_drive_packet(self, drive_commands):
        packet_list = []
        for command in drive_commands:
                wheelAddr, velocity, angle = command
                packet = BogiePacket(wheelAddr, velocity, angle)
                packet = packet.msg()  # Serializes packet
                packet_list.append(packet)
        return packet_list

    def assemble_arm_packets(self, arm_commands):
        packet_list = []
        for command in arm_commands:
                armAddr, secAddr, angle1, angle2 = command
                packet = ArmPacketLong(armAddr, secAddr, angle1, angle2)
                packet = packet.msg()  # Serializes packet
                packet_list.append(packet)
        return packet_list

    def assemble_stop_drive_packets(self):
        packet_list = []
        for wheelAddr in range(2,8):
                packet = BogiePacket(wheelAddr, 0, 0)
                packet = packet.msg()  # Serializes packet
                packet_list.append(packet)
        return packet_list

    def poll_drive_command(self):
        # Returns list of 6 tuples of drive commands in the form
        # (wheelAddr, velocity, angle)
        command_list = []
        for wheelAddr in range(2, 8):
            with self.roverStatusMutex:
                velocity = self.roverStatus.wheel_commands[wheelAddr - 2]['velo']
                angle = self.roverStatus.wheel_commands[wheelAddr - 2]['angle']
            cmd = wheelAddr, velocity, angle
            command_list.append(cmd)

        return command_list

    def poll_arm_command(self):
        # Returns list of 8 tuples of arm commands in the form
        # (armAddr, secAddr, data1, data2)
        # data1 could be degrees from 0 to 180
        # data2 could be degrees from 181 to 360
        # Primary Addresses are arm: 8 and wrist: 9
        # Secondary Addresses are Arm - shoulder: 1 and elbow: 2
        #                         Wrist - angle: 1, tilt: 2, scoop_actuate: 3,
        #                                 probe_actuate: 4, probe_data: 5 and
        #                                 voltage_data: 6
        command_list = []

        with self.roverStatus.roverStatusMutex:
            shoulder = self.roverStatus.arm_shoulder
            elbow = self.roverStatus.arm_elbow
            wrist_angle = self.roverStatus.wrist_angle
            wrist_tilt = self.roverStatus.wrist_tilt
            scoop_toggle = self.roverStatus.scoop_toggle
            voltage_toggle = self.roverStatus.voltage_toggle
            probe_toggle = self.roverStatus.probe_toggle
            probe_distance = self.roverStatus.probe_distance
        armAddr = 8
        wristAddr = 9

        # ARM COMMANDS
        # Shoulder
        angle_tuple = self.intToArmByte(shoulder)
        angle1, angle2 = angle_tuple
        cmd = armAddr, 1, angle1, angle2
        command_list.append(cmd)
        # Elbow
        angle_tuple = self.intToArmByte(elbow)
        angle1, angle2 = angle_tuple
        cmd = armAddr, 2, angle1, angle2
        command_list.append(cmd)

        ## WRIST COMMANDS
        ## Wrist Angle
        #angle_tuple = self.intToArmByte(wrist_angle)
        #angle1, angle2 = angle_tuple
        #cmd = wristAddr, 1, angle1, angle2
        #command_list.append(cmd)
        ## Wrist Tilt
        #angle = self.intToByte(wrist_tilt)
        #cmd = wristAddr, 2, angle
        #command_list.append(cmd)
        ## Scoop Actuate
        #if scoop_toggle is True:
        #    cmd = wristAddr, 3, 1
        #    command_list.append(cmd)
        #elif scoop_toggle is False:
        #    cmd = wristAddr, 3, 0
        #    command_list.append(cmd)
        ## Probe Actuate
        #distance = probe_distance
        #cmd = wristAddr, 4, distance
        #command_list.append(cmd)
        ## Probe Data
        #if probe_toggle is True:
        #    cmd = wristAddr, 5, 1   # Request
        #    command_list.append(cmd)
        #    with self.roverStatus.roverStatusMutex:
        #        self.roverStatus.probe_toggle = False # Reset Toggle
        ## Voltage Data
        #if voltage_toggle is True:
        #    cmd = wristAddr, 6, 1   # Request
        #    command_list.append(cmd)
        #    with self.roverStatus.roverStatusMutex:
        #        self.roverStatus.voltage_toggle = False # Reset Toggle

        return command_list