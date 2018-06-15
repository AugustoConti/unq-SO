#!/usr/bin/env python

from src.kernel import Kernel
from src.system.schedulers import SchedulerType
from src.hardware.mmu import *
from src.hardware.hardware import Hardware
from src.images import logo
from src.stats import run_stats
from src.utils import *


def run_simulator():
    memory_size = 32
    frame_size = 4
    count_frames = memory_size // frame_size
    sch = SchedulerType.choose()
    mmu = MMUType.choose()
    hardware = Hardware(memory_size, 0.1, mmu, frame_size)
    load_programs(hardware.disk())
    Kernel(hardware, sch, mmu, frame_size, count_frames)
    execute_programs(hardware.interrupt_vector())
    hardware.switch_on()


# TODO implementar PCB

# TODO agregar a STATS para cada pid, columna de retorno y espera
# TODO MultiThreading
# TODO Colores en logger de info
# TODO asignacion continua ?
# TODO implementar scheduler ShorterJobFirst !!
# TODO file system
# TODO proceso que empieze en un determinado tick

def runFcfsPaged():
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
    # runFcfsPaged()

    # logo()

    opt = input("1 - Statistics\n"
                "2 - Run simulator\n"
                "Choice: ")
    if opt == '1':
        run_stats()
    else:
        run_simulator()

    