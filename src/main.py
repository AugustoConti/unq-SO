#!/usr/bin/env python

from src.utils import *
from src.kernel import Kernel
from src.schedulers import *
from src.hardware import Hardware

# TODO MultiThreading
# TODO manejo de disco


def run_simulator():
    hardware = Hardware(35, 0.1)
    load_programs(hardware.disk())
    Kernel(hardware, choose_scheduler())
    execute_programs(hardware.interrupt_vector())
    hardware.switch_on()


if __name__ == '__main__':
    opt = input("1 - Estadísticas\n"
                "2 - Run simulator\n"
                "Opción: ")
    if opt == '1':
        logger.propagate = False

    logger.info('Starting emulator')

    if opt == '1':
        from src.stats import run_stats
        run_stats()
    else:
        run_simulator()
