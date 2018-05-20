#!/usr/bin/env python

from src.utils import load_programs, execute_programs
from src.kernel import Kernel
from src.schedulers import SchedulerType
from src.hardware import Hardware
from src.log import logger
from src.stats import run_stats


def run_simulator():
    hardware = Hardware(35, 0.1)
    load_programs(hardware.disk())
    Kernel(hardware, SchedulerType.choose())
    execute_programs(hardware.interrupt_vector())
    hardware.switch_on()


# TODO MultiThreading
if __name__ == '__main__':
    opt = input("1 - Statistics\n"
                "2 - Run simulator\n"
                "Choose: ")

    if opt == '1':
        logger.propagate = False
        run_stats()
    else:
        run_simulator()
