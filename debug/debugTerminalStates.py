import sys
import os
sys.path.append('/home/ubuntu/RoverBeagleBone/core')
import time
import threading
from threading import Lock

class debugTerminalStates(threading.Thread):
    def __init__(self, roverStatus):
        # Initializes threading
        threading.Thread.__init__(self)
        self.roverStatus = roverStatus

    def run(self):
        while 1:
            os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )
            with self.roverStatus.roverStatusMutex:
                ### ERROR STATES ###
                checksum_errors = self.roverStatus.checksum_errors
                unexpectedcontrolchar_errors = self.roverStatus.unexpectedcontrolchar_errors
                start_byte_errors = self.roverStatus.start_byte_errors
                ### ROVER ALIVE STATE ###
                roverAlive = self.roverStatus.roverAlive
                ### DRIVE STATES ###
                wheelAngle1 = self.roverStatus.wheel_commands[0]['angle']
                wheelAngle2 = self.roverStatus.wheel_commands[1]['angle']
                wheelAngle3 = self.roverStatus.wheel_commands[2]['angle']
                wheelAngle4 = self.roverStatus.wheel_commands[3]['angle']
                wheelAngle5 = self.roverStatus.wheel_commands[4]['angle']
                wheelAngle6 = self.roverStatus.wheel_commands[5]['angle']
                wheelVelo1 = self.roverStatus.wheel_commands[0]['velo']
                wheelVelo2 = self.roverStatus.wheel_commands[1]['velo']
                wheelVelo3 = self.roverStatus.wheel_commands[2]['velo']
                wheelVelo4 = self.roverStatus.wheel_commands[3]['velo']
                wheelVelo5 = self.roverStatus.wheel_commands[4]['velo']
                wheelVelo6 = self.roverStatus.wheel_commands[5]['velo']
                ### ARM STATES ###
                arm_shoulder = self.roverStatus.arm_shoulder
                arm_elbow = self.roverStatus.arm_elbow
                wrist_angle = self.roverStatus.wrist_angle
                wrist_tilt = self.roverStatus.wrist_tilt
                scoop_toggle = self.roverStatus.scoop_toggle
                voltage_toggle = self.roverStatus.voltage_toggle
                voltage_fresh_data = self.roverStatus.voltage_fresh_data
                voltage = self.roverStatus.voltage
                ####### TRIPOD STATES #######
                tri_hori = self.roverStatus.tri_hori
                tri_vert = self.roverStatus.tri_vert
                tri_zoom = self.roverStatus.tri_zoom
                ####### SCIENCE PROBE STATES #######
                probe_toggle = self.roverStatus.probe_toggle
                probe_distance = self.roverStatus.probe_distance
                probe_fresh_data = self.roverStatus.probe_fresh_data
                soil_moisture = self.roverStatus.soil_moisture
                conductivity = self.roverStatus.conductivity
                salinity = self.roverStatus.salinity
                f_temp = self.roverStatus.f_temp
                c_temp = self.roverStatus.c_temp
                ####### PACKAGE STATES #######
                package_one = self.roverStatus.package_one
                package_two = self.roverStatus.package_two
                package_three = self.roverStatus.package_three
                package_four = self.roverStatus.package_four
                package_five = self.roverStatus.package_five
                ####### MUX STATES #######
                mux_cam = self.roverStatus.mux_cam
                ####### GPS STATES #######
                utc_time = self.roverStatus.utc_time
		latitude = self.roverStatus.latitude
                longitude = self.roverStatus.longitude
                speed_gps = self.roverStatus.speed_gps
                nav_rec_warn = self.roverStatus.nav_rec_warn
                magnetic_var = self.roverStatus.magnetic_var

            # DISPLAY STATES
            print "|\tBEAGLEBONE\t|",                   "          MUX\t        |"
            print "| Alive: ", roverAlive, "\t\t|",     " Cam: ", mux_cam, "\t\t|"
            print "|_______________________|",          "______________________|"
            print "|     BOGIES VELOCITY\t|",           "\tSOIL PROBE\t|"
            print "| One:   ", wheelVelo1, "\t\t|",     " Moisture:  ", soil_moisture, "\t|"
            print "| Two:   ", wheelVelo2, "\t\t|",     " Conductiv: ", conductivity, "\t|"
            print "| Three: ", wheelVelo3, "\t\t|",     " Salinity:  ", salinity, "\t|"
            print "| Four:  ", wheelVelo4, "\t\t|",     " F-Temp:    ", f_temp, "\t|"
            print "| Five:  ", wheelVelo5, "\t\t|",     " C-Temp:    ", c_temp, "\t|"
            print "| Six:   ", wheelVelo6, "\t\t|",     "                      |"
            print "|_______________________|",          "______________________|"
            print "|      BOGIES ANGLE\t|",             "\tPACKAGES\t|"
            print "| One:   ", wheelAngle1, "\t\t|",    " One:    ", package_one, "\t|"
            print "| Two:   ", wheelAngle2, "\t\t|",    " Two:    ", package_two, "\t|"
            print "| Three: ", wheelAngle3, "\t\t|",    " Three:  ", package_three, "\t|"
            print "| Four:  ", wheelAngle4, "\t\t|",    " Four:   ", package_four, "\t|"
            print "| Five:  ", wheelAngle5, "\t\t|",    " Five:   ", package_five, "\t|"
            print "| Six:   ", wheelAngle6, "\t\t|",    "                      |"
            print "|_______________________|",          "______________________|"
            print "|          ARM          |",          "\t ERRORS \t|"
            print "| Shoulder:  ", arm_shoulder, "\t|", " CheckSum: ", checksum_errors, "\t|"
            print "| Elbow:     ", arm_elbow, "\t|",    " UnexCont: ", unexpectedcontrolchar_errors, "\t|"
            print "| WristAng:  ", wrist_angle, "\t|",  " StartByt: ", start_byte_errors, "\t|"
            print "| WristTilt: ", wrist_tilt, "\t|",   "______________________|"
            print "| ScoopActu: ", scoop_toggle, "\t|", "\t  GPS   \t|"
            print "| ProbeActu: ", probe_distance, "\t|"," Latitude: ", latitude, "\t|"
            print "| Probe Get: ", probe_toggle, "\t|", " Longitude: ", longitude, "\t|"
            print "| Probe New: ", probe_fresh_data, "\t|"," Speed: ", speed_gps, "\t|"
            print "| Volt Get:  ", voltage_toggle, "\t|"," Nav Rec Warn: ", nav_rec_warn, "\t|"
            print "| Volt New:  ", voltage_fresh_data, "\t|"," Magnetic Var: ", magnetic_var, "\t|"
            print "| Volt Val:  ", voltage, "\t|",      " UTC Time: ", utc_time, "\t|"
            print "|_______________________|"
            print "|        TRIPOD         |"
            print "| HoriServ: ", tri_hori, "\t\t|"
            print "| VertServ: ", tri_vert, "\t\t|"
            print "| Zoom:     ", tri_zoom, "\t\t|"
            print "|_______________________|"
            time.sleep(0.2)


