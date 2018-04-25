#!/usr/bin/env python

from src.so import *
from src.hardware import HARDWARE

class Timeline:
    def __init__(self, pcbTable):
        self._pcbTable = pcbTable
        self._tickNro = 1
        self._states = dict()

    def _terminated(self):
        for pcb in self._pcbTable:
            if pcb['state'] != STATE_TERMINATED:
                return False
        return True

    def _saveStates(self):
        pcbs = dict()
        for pcb in self._pcbTable:
            pcbs[pcb['pid']] = pcb['state']
        self._states[self._tickNro] = pcbs
        self._tickNro += 1

    def calculate(self):
        while(not self._terminated()):
            HARDWARE.clock.do_ticks(1)
            self._saveStates()


        print(self._states)



