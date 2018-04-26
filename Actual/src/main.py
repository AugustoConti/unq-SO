#!/usr/bin/env python

from src.utils import *
from src.so import Kernel
from src.stadistics import Timeline

# TODO linea de tiempo: como esta el sistema en cada tick
# TODO Calculo diagrama de gant, comprar scheduler
# TODO Threading
# TODO manejo de disco

if __name__ == '__main__':
    logger.propagate = False
    logger.info('Starting emulator')

    # setup our hardware and set memory size to 25 "cells"
    HARDWARE.setup(25)

    prg1 = expand([ASM.CPU(2), ASM.IO(), ASM.CPU(3), ASM.IO(), ASM.CPU(2)])
    prg2 = expand([ASM.CPU(4), ASM.IO(), ASM.CPU(1)])
    prg3 = expand([ASM.CPU(3)])

    # prg1 = expand([ASM.CPU(3)])
    # prg2 = expand([ASM.CPU(3)])
    # prg3 = expand([ASM.CPU(3)])

    HARDWARE.disk.add("prg1.exe", prg1)\
                 .add("prg2.exe", prg2)\
                 .add("prg3.exe", prg3)

    kernel = Kernel()

    stats = Timeline(kernel.pcbTable().pcbList)

    execute("prg1.exe", 3)
    execute("prg2.exe", 1)
    execute("prg3.exe", 5)

    stats.calc()

    #HARDWARE.switchOn()
