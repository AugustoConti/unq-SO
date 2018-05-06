#!/usr/bin/env python

from src.utils import *
from src.kernel import Kernel
from src.schedulers import *

# TODO linea de tiempo: como esta el sistema en cada tick
# TODO Calculo diagrama de gant, comparar scheduler
# TODO Threading
# TODO manejo de disco


def load_programs():
    HARDWARE.disk.add_all({
        'prg1.exe': expand([ASM.cpu(2), ASM.io(), ASM.cpu(3), ASM.io(), ASM.cpu(2)]),
        'prg2.exe': expand([ASM.cpu(4), ASM.io(), ASM.cpu(1)]),
        'prg3.exe': expand([ASM.cpu(3)]),
        'prg4.exe': expand([ASM.cpu(3)]),
        'prg5.exe': expand([ASM.cpu(3)]),
        'prg6.exe': expand([ASM.cpu(3)])
    })


def execute_programs():
    execute("prg1.exe", 3)
    execute("prg2.exe", 1)
    execute("prg3.exe", 5)
    execute("prg4.exe", 3)
    execute("prg5.exe", 1)
    execute("prg6.exe", 5)


def run_simulator(scheduler):
    Kernel(scheduler)
    execute_programs()
    HARDWARE.switch_on()


if __name__ == '__main__':
    opt = input("1 - Estadísticas\n"
                "2 - Run simulator\n"
                "Opción: ")
    if opt == '1':
        logger.propagate = False

    logger.info('Starting emulator')
    HARDWARE.setup(35)
    load_programs()

    sch_elegido = input("\n\nTipo de Scheduler:\n"
                        "1 - FCFS\n"
                        "2 - Priority No Expropiativo\n"
                        "3 - Priority Expropiativo\n"
                        "4 - Round Robin\n"
                        "Opción: ")

    sch = {'1': SchedulerType.fcfs(),
           '2': SchedulerType.priority_no_expropiativo(),
           '3': SchedulerType.priority_expropiativo(),
           '4': SchedulerType.round_robin()}[sch_elegido]

    if opt == '1':
        from src.stats import run_stats
        run_stats(sch)
    else:
        run_simulator(sch)
