# This bumps /dev/ttyO1, /dev/ttyO2, and /dev/ttyO4 into full duplex UART mode.
# Kind of hackish using system calls, but it just works.
#
# Check out the following link for a kick-ass tutorial
# http://www.gigamegablog.com/2012/01/22/beaglebone-coding-101-using-the-serial-and-analog-pins/
# NOTE: UART1 is /dev/ttyO1 and so on

import os

# uart0 is /dev/ttyO0 which is the miniUSB dev port
uart1 = [(0, "uart1_txd"), (20, "uart1_rxd")]
uart2 = [(1, "spi0_d0"), (21,"spi0_sclk")]
#uart3 = [(0, "???????"), (0, "?????????")]
uart4 = [(6, "gpmc_wpn"), (26, "gpmc_wait0")]
uart5 = [(24, "lcd_data9"), (4, "lcd_data8")]
uart_list = [uart1, uart2, uart4, uart5]

val_to_mux = []
for uart in uart_list:
	val_to_mux.append(uart[0])
	val_to_mux.append(uart[1])

for (val, mux) in val_to_mux:
        os.system("echo "+str(val)+" > /sys/kernel/debug/omap_mux/"+mux)
        os.system("cat /sys/kernel/debug/omap_mux/"+mux)
