#!/usr/bin/env python

from collections import defaultdict
from termcolor import colored
from src.interruption_handlers import *
from src.kernel import Kernel
from src.main import execute_programs

__all__ = ["run_stats"]


def run_stats(sch):
    kernel = Kernel(sch)
    execute_programs()
    Timeline(kernel.pcb_list()).calc()


class Timeline:
    def __init__(self, pcb_table):
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

    def __imprimir(self):
        print('\n', tabulate([['Letra', 'Estado'],
                              ['N', STATE_NEW],
                              ['R', STATE_READY],
                              ['X', STATE_RUNNING],
                              ['T', STATE_TERMINATED],
                              ['W', STATE_WAITING]], headers="firstrow"), '\n')
        print(tabulate(self._states, headers="keys", tablefmt="fancy_grid"))
        print('')
        print('Ready count: ', self._count_ready)
        print('Gant: ', self._count_ready / len(self._states[0]))

    def calc(self):
        while not self._terminated():
            self._save_states()
            HARDWARE.clock.do_ticks(1)
        self.__imprimir()
