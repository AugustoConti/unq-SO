#!/usr/bin/env python3
from src.hardware.hardware import Hardware
from src.hardware.mmu import *
from src.images import logo
from src.kernel import Kernel
from src.stats import run_stats
from src.system.schedulers import SchedulerType
from src.utils import *
from src.menu import *


# TODO al comienzo del simulador, limpiar pantalla y cartel con info del so (tipo sch, tipo mem, tamaño mem, etc)

# TODO proceso que empiece en un determinado tick
# TODO MultiThreading, 2 CPU ?? Tengo 2 running, Cada device en un thread?
# TODO asignacion continua ?
# TODO file system

# TODO COMANDOS: ps -a, mem, mostrame la memoria, tabla de paginas

# TODO TP: Introduccion, desarrollo y conclusion. Codigo en el PowerPoint.
# TODO INFORME con pros y contras del TP


def run_simulator():
    logger.enabled()
    memory_size = 12
    frame_size = 4
    count_frames = memory_size // frame_size
    sch = SchedulerType.choose()
    mmu = MMUType.choose()
    hardware = Hardware(memory_size, 1, mmu, frame_size)
    load_programs(hardware.disk())
    Kernel(hardware, sch, mmu, frame_size, count_frames)
    logger.indice()
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

    while True:
        opt = selection_menu(["Estadísticas", "Simulador", "Exit"], "Contillini OS")
        if opt == 2:
            return
        if opt in [0, 1]:
            {0: run_stats, 1: run_simulator}[opt]()


if __name__ == '__main__':
    main()
