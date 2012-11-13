########## Bus ##########

# Original Author: John Zeller

import serial, time

class Bus(object):
        def __init__(self):
                print "[%.4f] Opening Base Bus" % time.clock()
                self.base = serial.Serial(port='/dev/ttyO0',
                                        baudrate=115200)
                if self.base.isOpen():
                        print "[%.4f] ..........Success!" % time.clock()
                else:
                        print "[%.4f] ..........FAILED!" % time.clock()
                print "[%.4f] Opening Motor Bus" % time.clock()
                self.motor = serial.Serial(port='/dev/ttyO1',
                                        baudrate=115200)
                if self.motor.isOpen():
                        print "[%.4f] ..........Success!" % time.clock()
                else:
                        print "[%.4f] ..........FAILED!" % time.clock()
                print "[%.4f] Opening Tripod Bus" % time.clock()
                self.tripod = serial.Serial(port='/dev/ttyO2',
                                        baudrate=115200)
                if self.tripod.isOpen():
                        print "[%.4f] ..........Success!" % time.clock()
                else:
                        print "[%.4f] ..........FAILED!" % time.clock()
                print "[%.4f] Opening Arm Bus" % time.clock()
                self.arm = serial.Serial(port='/dev/ttyO4',
                                        baudrate=115200)
                if self.arm.isOpen():
                        print "[%.4f] ..........Success!" % time.clock()
                else:
                        print "[%.4f] ..........FAILED!" % time.clock()

        def restart(self, bus_name):
                if bus_name=='base':
                        self.base.close()
                        self.base = serial.Serial(port='/dev/ttyO0',
                                        baudrate=115200)
                elif bus_name=='motor':
                        self.motor.close()
                        self.motor = serial.Serial(port='/dev/ttyO1',
                                        baudrate=115200)
                elif bus_name=='tripod':
                        self.tripod.close()
                        self.tripod = serial.Serial(port='/dev/ttyO2',
                                        baudrate=115200)
                elif bus_name=='arm':
                        self.arm.close()
                        self.arm = serial.Serial(port='/dev/ttyO4',
                                        baudrate=115200)
                elif bus_name=='all':
                        self.restart('base')
                        self.restart('motor')
                        self.restart('tripod')
                        self.restart('arm')
