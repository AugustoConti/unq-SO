from so import *

if __name__ == '__main__':
    logger.info('Starting emulator')

    # setup our hardware and set memory size to 25 "cells"
    HARDWARE.setup(25)

    prg1 = Expand([ASM.CPU(2), ASM.IO(), ASM.CPU(3), ASM.IO(), ASM.CPU(2)]).expand()
    prg2 = Expand([ASM.CPU(4), ASM.IO(), ASM.CPU(1)]).expand()
    prg3 = Expand([ASM.CPU(3)]).expand()

    HARDWARE.disc.add("prg1.exe", prg1).add("prg2.exe", prg2).add("prg3.exe", prg3)

    kernel = Kernel()

    kernel.execute("prg1.exe", 5)
    kernel.execute("prg2.exe", 8)
    kernel.execute("prg3.exe", 1)

    HARDWARE.switchOn()
