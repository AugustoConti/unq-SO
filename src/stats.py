from collections import defaultdict
from pydoc import pipepager

from tabulate import tabulate
from termcolor import colored

from src.configuration.mmu_factory import AsignacionContinuaFactory
from src.configuration.scheduler import SchedulerType
from src.hardware.hardware import *
from src.kernel import Kernel
from src.structures.states import State
from src.utils.log import logger
from src.utils.utils import execute_programs

__all__ = ["run_stats"]


def run_stats():
    logger.disabled()
    salida = '\n'+State.map_all()+'\n'
    total = [['Scheduler', 'Return', 'Wait']]
    mmu_type = AsignacionContinuaFactory
    for scheduler in SchedulerType.all():
        salida += '\n\n'+colored(SchedulerType.str(scheduler), 'cyan')+'\n'
        hardware = Hardware(50, 0, mmu_type, 1)
        kernel = Kernel(hardware, scheduler, mmu_type, 0, 0, 2, None)
        execute_programs(hardware.interrupt_vector())
        tabla, gant = Timeline(hardware, kernel.pcb_list()).calc()
        salida += tabla
        total.append([SchedulerType.str(scheduler)] + gant)
    salida += '\n\n'+tabulate(total, headers="firstrow", tablefmt="presto")+'\n'
    pipepager(salida, cmd='less -R -S')


class Timeline:
    def __init__(self, hard, pcb_table):
        self._hard = hard
        self._pcb_table = pcb_table
        self._tick_nro = 0
        self._ready = defaultdict(int)
        self._retorno = defaultdict(int)
        self._states = defaultdict(list)

    def _terminated(self):
        return all(pcb.state == State.TERMINATED for pcb in self._pcb_table)

    def _save_states(self):
        self._states[self._tick_nro - 1] = ['PCB ' + str(pcb.pid) for pcb in self._pcb_table] if self._tick_nro == 0 \
            else [State.mapear(pcb.state) for pcb in self._pcb_table]
        if self._tick_nro > 0:
            for pcb in self._pcb_table:
                self._retorno[pcb.pid] += 1 if pcb.state != State.TERMINATED else 0
                self._ready[pcb.pid] += 1 if pcb.state == State.READY else 0
        self._tick_nro += 1

    def calc(self):
        while not self._terminated():
            self._save_states()
            self._hard.tick()
        self._states['Return'] = self._retorno.values()
        self._states['Wait'] = self._ready.values()
        total_retorno = sum(self._retorno.values())
        total_espera = sum(self._ready.values())
        return (tabulate(self._states, headers="keys", tablefmt="fancy_grid"),
                [round(total_retorno / len(self._pcb_table), 2), round(total_espera / len(self._pcb_table), 2)])
