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
        self.waitTime = 0.1  # Wait 20ms between packet cycles
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
