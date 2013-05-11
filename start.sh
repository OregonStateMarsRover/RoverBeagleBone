#!/bin/bash

echo "Removing all .pyc files";
rm -r /home/ubuntu/*.pyc

echo "Starting Receptionist";
python /home/ubuntu/RoverBeagleBone/receptionist.py &
