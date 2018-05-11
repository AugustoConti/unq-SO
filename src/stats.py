#!/usr/bin/env python

from collections import defaultdict
from termcolor import colored
from src.interruption_handlers import *
from src.kernel import Kernel
from src.schedulers import all_schedulers, SchedulerType
from src.utils import *

__all__ = ["run_stats"]


def run_stats():
    print('\n', tabulate([['Letra', 'Estado'],
                          ['N', STATE_NEW],
                          ['R', STATE_READY],
                          ['X', STATE_RUNNING],
                          ['T', STATE_TERMINATED],
                          ['W', STATE_WAITING]], headers="firstrow"), '\n')
    total = [['Scheduler', 'Ready', 'Gant']]
    for scheduler in all_schedulers:
        print('\n', colored(SchedulerType.str(scheduler), 'cyan'))
        hardware = Hardware(35, 0)
        load_programs(hardware.disk())
        kernel = Kernel(hardware, scheduler)
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
        self._count_ready = 0
        self._states = defaultdict(list)

    def _terminated(self):
        return all(pcb['state'] == STATE_TERMINATED for pcb in self._pcb_table)

    def _save_states(self):
        self._states[self._tick_nro] = [pcb['pid'] for pcb in self._pcb_table] if self._tick_nro == 0 \
            else [self.__mapear(pcb['state']) for pcb in self._pcb_table]
        self._count_ready += self._states[self._tick_nro].count(self.__mapear(STATE_READY))
        self._tick_nro += 1

    def __mapear(self, state):
        return {
            STATE_NEW: colored('N', 'magenta'),
            STATE_READY: colored('R', 'green'),
            STATE_RUNNING: colored('X', 'red'),
            STATE_TERMINATED: colored('T', 'white'),
            STATE_WAITING: colored('W', 'cyan')
        }[state]

    def calc(self):
        while not self._terminated():
            self._save_states()
            self._clock.do_ticks(1)
        print(tabulate(self._states, headers="keys", tablefmt="fancy_grid"))
        return [self._count_ready, self._count_ready / len(self._pcb_table)]
