#!/usr/bin/env python

from src.hardware.hardware import Hardware
from src.hardware.mmu import *
from src.images import logo
from src.kernel import Kernel
from src.stats import run_stats
from src.system.schedulers import SchedulerType
from src.utils import *
from src.menu import *
from consolemenu import *
from consolemenu.items import *

def run_simulator():
    memory_size = 12
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

# TODO en logger, indice de que es cada color al principio de simulacion
# TODO al comienzo del simulador, limpiar pantalla y cartel con info del so (tipo sch, tipo mem, tamaño mem, etc)

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
    logo()
    menu = ConsoleMenu("Contillini OS", formatter=menu_format)
    menu.append_item(FunctionItem("Estadísticas", run_stats))
    menu.append_item(FunctionItem("Simulador", run_simulator))
    menu.show()
