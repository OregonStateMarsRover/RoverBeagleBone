#!/bin/bash

# Still Camera - pin39.P8
# Front Package 1 - GND, 1, 2, 3: (1 - pin44.P8), (2 - pin41.P8), (3 - pin42.P8)
# Back Package 2 - GND, 4, 5, 6: (3 - pin45.P8), (4 - pin46.P8), (5 - pin43.P8)

# PIN - GPIO
# 1 - GPIO2_9 = 2 * 32 + 9 = 73
# 2 - GPIO2_10 = 2 * 32 + 10 = 74
# 3 - GPIO2_11 = 2 * 32 + 11 = 75
# 4 - GPIO2_6 = 2 * 32 + 6 = 70
# 5 - GPIO2_7 = 2 * 32 + 7 = 71
# 6 - GPIO2_8 = 2 * 32 + 8 = 72

# Setup GPIO files
echo 73 > /sys/class/gpio/export	# Setup Package GPIO 1
echo 74 > /sys/class/gpio/export	# Setup Package GPIO 2
echo 75 > /sys/class/gpio/export	# Setup Package GPIO 3
echo 70 > /sys/class/gpio/export	# Setup Package GPIO 4
echo 71 > /sys/class/gpio/export	# Setup Package GPIO 5
echo 72 > /sys/class/gpio/export	# Setup Package GPIO 6
echo "All GPIO files setup"

# Set all GPIO pins to output
echo out > /sys/class/gpio/gpio73/direction	# GPIO 1 set to output
echo out > /sys/class/gpio/gpio74/direction	# GPIO 2 set to output
echo out > /sys/class/gpio/gpio75/direction	# GPIO 3 set to output
echo out > /sys/class/gpio/gpio70/direction	# GPIO 4 set to output
echo out > /sys/class/gpio/gpio71/direction	# GPIO 5 set to output
echo out > /sys/class/gpio/gpio72/direction	# GPIO 6 set to output
echo "All GPIO pins set to output"

# Go into infinite loop and set all pins to on and off
for (( ; ; ))
do
        echo 1 > /sys/class/gpio/gpio73/value	# GPIO 1 set to high
        echo 1 > /sys/class/gpio/gpio74/value	# GPIO 2 set to high
        echo 1 > /sys/class/gpio/gpio75/value	# GPIO 3 set to high
        echo 1 > /sys/class/gpio/gpio70/value	# GPIO 4 set to high
        echo 1 > /sys/class/gpio/gpio71/value	# GPIO 5 set to high
        echo 1 > /sys/class/gpio/gpio72/value	# GPIO 6 set to high
        echo "All GPIOs set to HIGH!"
        sleep 3
        echo 0 > /sys/class/gpio/gpio73/value	# GPIO 1 set to high
        echo 0 > /sys/class/gpio/gpio74/value	# GPIO 2 set to high
        echo 0 > /sys/class/gpio/gpio75/value	# GPIO 3 set to high
        echo 0 > /sys/class/gpio/gpio70/value	# GPIO 4 set to high
        echo 0 > /sys/class/gpio/gpio71/value	# GPIO 5 set to high
        echo 0 > /sys/class/gpio/gpio72/value	# GPIO 6 set to high
        echo "All GPIOs set to LOW!"
        sleep 3
done
