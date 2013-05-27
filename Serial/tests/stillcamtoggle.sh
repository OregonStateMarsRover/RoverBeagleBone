#!/bin/bash

echo 76 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio76/direction
for (( ; ; ))
do
        echo 1 > /sys/class/gpio/gpio76/value
        echo "High!"
        sleep 5
        echo 0 > /sys/class/gpio/gpio76/value
        echo "Low!"
        sleep 5
done
