########## Bus ##########

# Original Author: John Zeller

# Bus initializes every port for use on the BeagleBone, and offers
# them up as easy to access attributes. Additionally, there is the
# option to reset any or all ports by using the restart function.

import serial


class Bus(object):
    def __init__(self):
        self.base = serial.Serial(port='/dev/ttyO5',
                                  baudrate=115200)
        self.arm = serial.Serial(port='/dev/ttyO1',
                                 baudrate=115200)
        self.tripod = serial.Serial(port='/dev/ttyO2',
                                    baudrate=115200)
        self.drive = serial.Serial(port='/dev/ttyO4',
                                   baudrate=115200)

    def restart(self, bus_name):
        if bus_name == 'base':
            self.base.close()
            self.base = serial.Serial(port='/dev/ttyO0',
                                      baudrate=115200)
        elif bus_name == 'arm':
            self.arm.close()
            self.arm = serial.Serial(port='/dev/ttyO1',
                                     baudrate=115200)
        elif bus_name == 'tripod':
            self.tripod.close()
            self.tripod = serial.Serial(port='/dev/ttyO2',
                                        baudrate=115200)
        elif bus_name == 'drive':
            self.drive.close()
            self.drive = serial.Serial(port='/dev/ttyO4',
                                       baudrate=115200)
        elif bus_name == 'all':
            self.restart('base')
            self.restart('drive')
            self.restart('tripod')
            self.restart('arm')
