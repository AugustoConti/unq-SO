from so import *

if __name__ == '__main__':
    logger.info('Starting emulator')

    # setup our hardware and set memory size to 25 "cells"
    HARDWARE.setup(25)

    prg1 = Program("prg1.exe", [ASM.CPU(2), ASM.IO(), ASM.CPU(3), ASM.IO(), ASM.CPU(2)])
    prg2 = Program("prg2.exe", [ASM.CPU(4), ASM.IO(), ASM.CPU(1)])
    prg3 = Program("prg3.exe", [ASM.CPU(3)])

    HARDWARE.disc.add(prg1).add(prg2).add(prg3)

    kernel = Kernel()

    kernel.execute("prg1.exe")
    kernel.execute("prg2.exe")
    kernel.execute("prg3.exe")

    HARDWARE.switchOn()
