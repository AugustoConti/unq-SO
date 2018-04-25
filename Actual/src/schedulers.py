#!/usr/bin/env python

from src.hardware import HARDWARE
from src.log import logger
from src.interruptionHandlers import *

class FCFS:
    def __init__(self):
        self._ready = []

    def isEmpty(self):
        return not self._ready

    def add(self, pid):
        self._ready.append(pid)

    def next(self):
        return self._ready.pop(0)


class PriorityNoExp:
    def __init__(self, pcbTable):
        self.__cantPriority = 5
        self.__doAging = 0
        self._pcbTable = pcbTable
        self._ready = []
        for i in range(self.__cantPriority):
            self._ready.append([])

    def isEmpty(self):
        for plist in self._ready:
            if plist:
                return False
        return True

    def __getMaxPriority(self):
        for plist in self._ready:
            if plist:
                return plist.pop(0)

    def __aging(self):
        self.__doAging += 1
        if self.__doAging % 4 == 0:
            for i in range(1, self.__cantPriority - 1):
                if self._ready[i]:
                    self._ready[i-1].append(self._ready[i].pop(0))

    def next(self):
        pid = self.__getMaxPriority()
        self.__aging()
        return pid

    def add(self, pid):
        self._ready[self._pcbTable.getPriority(pid)-1].append(pid)


class PriorityExp:
    def __init__(self, pcbTable, dispatcher, base):
        self._pcbTable = pcbTable
        self._dispatcher = dispatcher
        self._base = base

    def isEmpty(self):
        return self._base.isEmpty()

    def add(self, pid):
        pcbRun = self._pcbTable.getRunning()
        if self._pcbTable.getPriority(pid) < pcbRun['priority']:
            self._dispatcher.save()
            self._dispatcher.load(pid)
            self._base.add(pcbRun['pid'])
            logger.info("PCB entrante con mayor prioridad que running!")
        else:
            self._base.add(pid)

    def next(self):
        return self._base.next()


class RoundRobin:
    def __init__(self, base, quantum):
        HARDWARE.timer.start(quantum)
        self._base = base

    def isEmpty(self):
        return self._base.isEmpty()

    def add(self, pid):
        self._base.add(pid)

    def next(self):
        return self._base.next()


class Scheduler:
    def __init__(self, pcbTable, dispatcher, tipo):
        self.__tipo = tipo
        self._pcbTable = pcbTable
        self._dispatcher = dispatcher

    def __add(self, pid):
        self.__tipo.add(pid)
        self._pcbTable.getPCB(pid)['state'] = STATE_READY

    def addRunning(self):
        self.__add(self._pcbTable.getRunningPid())

    def runOrAddQueue(self, pid):
        if self._pcbTable.isRunning():
            self.__add(pid)
        else:
            self._dispatcher.load(pid)

    def loadFromReady(self):
        self._pcbTable.setRunning(None)
        HARDWARE.timer.stop()
        if not self.__tipo.isEmpty():
            self._dispatcher.load(self.__tipo.next())
