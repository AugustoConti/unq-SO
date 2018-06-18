from collections import defaultdict

from termcolor import colored

from src.hardware.hardware import *
from src.kernel import Kernel
from src.log import Logger
from src.system.schedulers import SchedulerType
from src.system.states import State
from src.utils import *

__all__ = ["run_stats"]


def mapear(state):
    return {
        State.NEW: colored('N', 'magenta'),
        State.READY: colored('R', 'green'),
        State.RUNNING: colored(' X ', 'red', attrs=['reverse']),
        State.TERMINATED: colored('T', 'white'),
        State.WAITING: colored('W', 'cyan')
    }[state]


def run_stats():
    Logger.disabled()
    print('\n', tabulate([['Letra', 'Estado'],
                          ['N', State.NEW],
                          ['R', State.READY],
                          ['X', State.RUNNING],
                          ['T', State.TERMINATED],
                          ['W', State.WAITING]], headers="firstrow"), '\n')
    total = [['Scheduler', 'Retorno', 'Ready']]
    for scheduler in SchedulerType.all():
        print('\n', colored(SchedulerType.str(scheduler), 'cyan'))
        hardware = Hardware(50, 0, 0, 1)
        load_programs(hardware.disk())
        kernel = Kernel(hardware, scheduler, 0, 0, 0)
        execute_programs(hardware.interrupt_vector())

        gant = Timeline(hardware.clock(), kernel.pcb_list()).calc()
        total.append([SchedulerType.str(scheduler)] + gant)
    print('\n')
    print(tabulate(total, headers="firstrow", tablefmt="presto"))


class Timeline:
    def __init__(self, clock, pcb_table):
        self._clock = clock
        self._pcb_table = pcb_table
        self._tick_nro = 0
        self._ready = defaultdict(int)
        self._retorno = defaultdict(int)
        self._states = defaultdict(list)

    def _terminated(self):
        return all(pcb.state == State.TERMINATED for pcb in self._pcb_table)

    def _save_states(self):
        self._states[self._tick_nro] = ['PCB ' + str(pcb.pid) for pcb in self._pcb_table] if self._tick_nro == 0 \
            else [mapear(pcb.state) for pcb in self._pcb_table]
        if self._tick_nro > 0:
            for pcb in self._pcb_table:
                self._retorno[pcb.pid] += 1 if pcb.state != State.TERMINATED else 0
                self._ready[pcb.pid] += 1 if pcb.state == State.READY else 0
        self._tick_nro += 1

    def calc(self):
        while not self._terminated():
            self._save_states()
            self._clock.do_ticks(1)
        self._states['Retorno'] = self._retorno.values()
        self._states['Espera'] = self._ready.values()
        totalEspera = sum(self._ready.values())
        totalRetorno = sum(self._ready.values())
        print(tabulate(self._states, headers="keys", tablefmt="fancy_grid"))
        return [totalRetorno / len(self._pcb_table), totalEspera / len(self._pcb_table)]
