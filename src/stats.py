from tabulate import tabulate
from termcolor import colored

from src.configuration.mmu_factory import AsignacionContinuaFactory
from src.configuration.scheduler import SchedulerType
from src.hardware.hardware import *
from src.kernel import Kernel
from src.structures.states import State
from src.utils import sound
from src.utils.log import logger
from src.utils.utils import show_less, Executor

__all__ = ["run_stats"]


def run_stats():
    logger.disabled()
    sound.habilitado = False
    salida = '\n' + State.map_all() + '\n'
    total = [['Scheduler', 'Return', 'Wait']]
    mmu_type = AsignacionContinuaFactory
    for scheduler in SchedulerType.all():
        salida += '\n\n' + colored(SchedulerType.str(scheduler), 'cyan') + '\n'
        hardware = Hardware(50, 0, mmu_type, 1)
        kernel = Kernel(hardware, scheduler, mmu_type, 0, 0, 2, None)
        execute_programs(hardware.clock_cpu(), hardware.interrupt_vector())
        hardware.tick()
        while any(pcb.state != State.TERMINATED for pcb in kernel.pcb_list()):
            hardware.tick()
        tabla, gant = kernel.gant()
        salida += tabla
        total.append([SchedulerType.str(scheduler)] + gant)
    salida += '\n\n' + tabulate(total, headers="firstrow", tablefmt="presto") + '\n'
    show_less(salida)


def execute_programs(clock, interrupt_vector):
    Executor(clock, interrupt_vector, 'fifa', 0, 3)
    Executor(clock, interrupt_vector, 'cs', 3, 1)
    Executor(clock, interrupt_vector, 'book', 0, 5)
    Executor(clock, interrupt_vector, 'calc', 5, 5)
    Executor(clock, interrupt_vector, 'xls', 7, 4)
    Executor(clock, interrupt_vector, 'git', 5, 3)
