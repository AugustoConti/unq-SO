#!/usr/bin/env python

from src.utils import load_programs, execute_programs
from src.kernel import Kernel
from src.schedulers import SchedulerType
from src.mmu import *
from src.hardware import Hardware
from src.log import logger
from src.stats import run_stats


def run_simulator():
    sch = SchedulerType.choose()
    mmu = MMUType.choose()
    if mmu > 0:
        frame_size = int(input("\n\nFrame size:"))
    else:
        frame_size = 0
    hardware = Hardware(35, 0.1, mmu, frame_size)
    load_programs(hardware.disk())
    Kernel(hardware, sch, mmu, frame_size)
    execute_programs(hardware.interrupt_vector())
    hardware.switch_on()


# TODO MultiThreading
if __name__ == '__main__':
    opt = input("1 - Statistics\n"
                "2 - Run simulator\n"
                "Choice: ")
    if opt == '1':
        run_stats()
    else:
        run_simulator()
