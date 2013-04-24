#############################
# File Name: rover_status.py
# Author: Cameron Bowie
# Date: 2/7/13
# Description: A class to hold the rover variables. Designed to ease rover-gui interaction
#############################

import math

class RoverStatus():
    # Error Tracking
    checksum_errors  = 0
    unexpectedcontrolchar_errors = 0
    start_byte_errors = 0

    roverAlive = 0

    wheel_commands = [{}, {}, {}, {}, {}, {}]

    wheel_commands[0]['angle'] = 0
    wheel_commands[1]['angle'] = 0
    wheel_commands[2]['angle'] = 0
    wheel_commands[3]['angle'] = 0
    wheel_commands[4]['angle'] = 0
    wheel_commands[5]['angle'] = 0

    wheel_commands[0]['velo'] = 0
    wheel_commands[1]['velo'] = 0
    wheel_commands[2]['velo'] = 0
    wheel_commands[3]['velo'] = 0
    wheel_commands[4]['velo'] = 0
    wheel_commands[5]['velo'] = 0

    ####### ARM CONTROL STATES #######

    # Value Constants for Arm
    initShoulderAngle = 110
    initElbowAngle = 20
    initWristAngle = 330
    shoulderMin = 0
    shoulderMax = 120
    elbowMin = 10
    elbowMax = 350
    wristMin = 10
    wristMax = 350

    arm_shoulder = 0.0
    arm_elbow = 0.0

    wrist_angle = 0.0
    wrist_tilt = 0.0  # From -90 to 90

    scoop_toggle = False
    voltage_toggle = False
    voltage_fresh_data = False
    voltage = 0

    ####### TRIPOD CONTROL STATES #######
    tri_hori = 0
    tri_vert = 0
    tri_zoom = 0

    ####### SCIENCE PROBE CONTROL STATES #######
    probe_toggle = False
    probe_distance = 0
    probe_fresh_data = False

    soil_moisture = 0
    conductivity = 0
    salinity = 0
    f_temp = 0
    c_temp = 0

    ####### PACKAGE CONTROL STATES #######
    packages = ["package_one", "package_two", "package_three"]
    packages += ["package_four", "package_five"]
    package_one = False
    package_two = False
    package_three = False
    package_four = False
    package_five = False

    ####### MUX CONTROL STATES #######
    mux_cam = 1 # 1-4 - Default is 1 "Main Camera"