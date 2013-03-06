#############################
# File Name: rover_status.py
# Author: John Zeller
# Date: 3/5/13
# Description: A class to hold the rover variables
#############################

class RoverStatus():
    roverAlive = 0

    # Drive Variables
    # TODO: make wheels 2 to 7 (starting with front left, ending with rear right)

    # Commanded Values - ie What comes as commands from base
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

    # Actual Values - ie What is actually happening, based on the encoders
    #wheel_actual = [{}, {}, {}, {}, {}, {}]

    #wheel_actual[0]['angle'] = 0
    #wheel_actual[1]['angle'] = 0
    #wheel_actual[2]['angle'] = 0
    #wheel_actual[3]['angle'] = 0
    #wheel_actual[4]['angle'] = 0
    #wheel_actual[5]['angle'] = 0

    #wheel_actual[0]['velo'] = 0
    #wheel_actual[1]['velo'] = 0
    #wheel_actual[2]['velo'] = 0
    #wheel_actual[3]['velo'] = 0
    #wheel_actual[4]['velo'] = 0
    #wheel_actual[5]['velo'] = 0


    # Arm Variables
    #tri_hori = 0
    #tri_vert = 0
    #tri_zoom = 0

    #arm_seg = [{}, {}, {}]

    # Arm segment lengths
    #arm_seg[0]['len'] = 1.4
    #arm_seg[1]['len'] = 1.3
    #arm_seg[2]['len'] = 1.0

    #wrist_angle = 0
    #wrist_tilt = 0

    #scoop_open = False
    #svoltage = 0