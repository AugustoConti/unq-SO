#!/usr/bin/env python

from src.so import *
from src.hardware import HARDWARE
from collections import defaultdict
from tabulate import tabulate

class Timeline:
    def __init__(self, pcbTable):
        self._pcbTable = pcbTable
        self._tickNro = 1
        self._states = defaultdict(list)

    def _terminated(self):
        for pcb in self._pcbTable:
            if pcb['state'] != STATE_TERMINATED:
                return False
        return True

    def _saveStates(self):
        for pcb in self._pcbTable:
            self._states[pcb['pid']].append(pcb['state'])
        self._tickNro += 1

    def __mapear(self, state):
        return {
            STATE_NEW: 'N',
            STATE_READY: '\033[92m'+'R',
            STATE_RUNNING: '\033[95m'+'X',
            STATE_TERMINATED: 'T',
            STATE_WAITING: '\033[94m'+'W',
        }[state] + '\033[0m'

    def __imprimir(self):
        print('')
        print(tabulate([['Letra','Estado'],['N', STATE_NEW],['R', STATE_READY],['X', STATE_RUNNING],['T', STATE_TERMINATED]
                     ,['W', STATE_WAITING]], headers="firstrow"))

        print('')
        print('')

        print('\033[93m', 'PID    ', end="")
        for i in range(1, self._tickNro):
            print("%02d" % i,' ', end="")
        print('')
        for pid, states in self._states.items():
            print(' ', '\033[93m', pid, ' ', end="")
            for s in states:
                print(' ', self.__mapear(s), '', end="")
            print('')

    def __calculate(self):
        count = 0
        for pid, states in self._states.items():
            for s in states:
                if s == STATE_READY:
                    count += 1
        print('')
        print('Cantidad de Ready: ', count)
        print('Gant: ', count / len(self._states.keys()))

    def calc(self):
        while(not self._terminated()):
            HARDWARE.clock.do_ticks(1)
            self._saveStates()
        self.__imprimir()
        self.__calculate()

