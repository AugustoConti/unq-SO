#!/usr/bin/env python
from src.kernel import Kernel
from src.system.schedulers import SchedulerType
from src.hardware.mmu import *
from src.hardware.hardware import Hardware
from src.images import logo
from src.stats import run_stats
from src.utils import *


def run_simulator():
    memory_size = 8
    frame_size = 4
    count_frames = memory_size // frame_size
    sch = SchedulerType.choose()
    mmu = MMUType.choose()
    hardware = Hardware(memory_size, 0.1, mmu, frame_size)
    load_programs(hardware.disk())
    Kernel(hardware, sch, mmu, frame_size, count_frames)
    execute_programs(hardware.interrupt_vector())
    hardware.switch_on()


# TODO MultiThreading
if __name__ == '__main__':
    logo()
    opt = input("1 - Statistics\n"
                "2 - Run simulator\n"
                "Choice: ")
    if opt == '1':
        run_stats()
    else:
        run_simulator()
