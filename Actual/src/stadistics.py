#!/usr/bin/env python

from src.so import *
from src.hardware import HARDWARE
from collections import defaultdict
from tabulate import tabulate
from termcolor import colored, cprint

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
            STATE_NEW: colored('N', 'magenta'),
            STATE_READY: colored('R', 'green'),
            STATE_RUNNING: colored('X', 'red'),
            STATE_TERMINATED: colored('T', 'white'),
            STATE_WAITING: colored('W', 'cyan')
        }[state]

   # text =
   # print(text)
   # cprint('Hello, World!', 'green')

    def __imprimir(self):
        count = 0
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
                count += 1 if s == STATE_READY else 0
                print(' ', self.__mapear(s), '', end="")
            print('')
        print('')
        print('Cantidad de Ready: ', count)
        print('Gant: ', count / len(self._states.keys()))

    def calc(self):
        while(not self._terminated()):
            HARDWARE.clock.do_ticks(1)
            self._saveStates()
        self.__imprimir()

