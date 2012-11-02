# This bumps /dev/ttyO1, /dev/ttyO2, and /dev/ttyO4 into full duplex UART mode.
# Kind of hackish using system calls, but it just works.
#
# Check out the following link for a kick-ass tutorial
# http://www.gigamegablog.com/2012/01/22/beaglebone-coding-101-using-the-serial-and-analog-pins/

import os

val_to_mux = [(0, "uart1_txd"), (20, "uart1_rxd"), (1, "spi0_d0")]
val_to_mux += [(21,"spi0_sclk"), (6, "gpmc_wpn"), (26, "gpmc_wait0")]

for (val, mux) in val_to_mux:
        os.system("echo "+str(val)+" > /sys/kernel/debug/omap_mux/"+mux)
        os.system("cat /sys/kernel/debug/omap_mux/"+mux)
