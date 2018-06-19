#!/usr/bin/env python

from src.hardware.hardware import Hardware
from src.hardware.mmu import *
from src.kernel import Kernel
from src.stats import run_stats
from src.system.schedulers import SchedulerType
from src.utils import *


def run_simulator():
    memory_size = 16
    frame_size = 4
    count_frames = memory_size // frame_size
    sch = SchedulerType.choose()
    mmu = MMUType.choose()
    hardware = Hardware(memory_size, 0.1, mmu, frame_size)
    load_programs(hardware.disk())
    Kernel(hardware, sch, mmu, frame_size, count_frames)
    execute_programs(hardware.interrupt_vector())
    hardware.switch_on()


# TODO Colores en logger de info

# TODO Second chance, ordenar por frame, guardar aguja en ultimo frame

# TODO proceso que empieze en un determinado tick
# TODO MultiThreading
# TODO asignacion continua ?
# TODO file system


def run_fcfs_paged():
    memory_size = 32
    frame_size = 4
    count_frames = memory_size // frame_size
    mmu = 2
    hardware = Hardware(memory_size, 0.1, mmu, frame_size)
    load_programs(hardware.disk())
    Kernel(hardware, 0, mmu, frame_size, count_frames)
    execute_programs(hardware.interrupt_vector())
    hardware.switch_on()


if __name__ == '__main__':
    # run_fcfs_paged()

    # logo()

    opt = input("1 - Statistics\n"
                "2 - Run simulator\n"
                "Choice: ")
    if opt == '1':
        run_stats()
    else:
        run_simulator()
