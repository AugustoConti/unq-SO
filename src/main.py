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


# TODO Colores en logger de info

# TODO al comienzo del simulador, limpiar pantalla y cartel con info del so (tipo sch, tipo mem, tamaño mem, etc)

# TODO proceso que empieze en un determinado tick
# TODO MultiThreading, 2 CPU ?? Tengo 2 running, Cada device en un thread?
# TODO asignacion continua ?
# TODO file system

# TODO comandos ps -a, mem, mostrame la memoria, tabla de paginas

# TODO TP: Introduccion, desarrollo y conclusion. Codigo en el PowerPoint.
# TODO Informe con pros y contras del TP


def run_simulator():
    memory_size = 12
    frame_size = 4
    count_frames = memory_size // frame_size
    sch = SchedulerType.choose()
    mmu = MMUType.choose()
    hardware = Hardware(memory_size, 0.1, mmu, frame_size)
    load_programs(hardware.disk())
    Kernel(hardware, sch, mmu, frame_size, count_frames)
    clear_screen()
    Logger.indice()
    execute_programs(hardware.interrupt_vector())
    hardware.switch_on()


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


def main():
    # run_fcfs_paged()
    logo()
    menu = ConsoleMenu("Contillini OS", formatter=menu_format)
    menu.append_item(FunctionItem("Estadísticas", run_stats))
    menu.append_item(FunctionItem("Simulador", run_simulator))
    menu.show()


if __name__ == '__main__':
    main()
