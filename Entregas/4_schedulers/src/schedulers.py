#!/usr/bin/env python

from src.log import logger
from src.interruption_handlers import STATE_READY


class SchedulerType:
    @staticmethod
    def fcfs():
        return 0

    @staticmethod
    def priority_no_expropiativo():
        return 1

    @staticmethod
    def priority_expropiativo():
        return 2

    @staticmethod
    def round_robin():
        return 3


class FCFS:
    def __init__(self):
        self._ready = []

    def is_empty(self):
        return not self._ready

    def add(self, pid):
        self._ready.append(pid)

    def next(self):
        return self._ready.pop(0)


class PriorityNoExp:
    def __init__(self, pcb_table):
        self.__cant_priority = 5
        self.__doAging = 0
        self._pcb_table = pcb_table
        self._ready = [[] for x in range(self.__cant_priority)]

    def is_empty(self):
        return not any(self._ready)

    def __get_max_priority(self):
        for plist in self._ready:
            if plist:
                return plist.pop(0)

    def __aging(self):
        self.__doAging += 1
        if self.__doAging % 4 == 0:
            [self._ready[i-1].append(self._ready[i].pop(0)) for i in range(1, self.__cant_priority) if self._ready[i]]

    def next(self):
        pid = self.__get_max_priority()
        self.__aging()
        return pid

    def add(self, pid):
        self._ready[self._pcb_table.get_priority(pid)-1].append(pid)


class PriorityExp:
    def __init__(self, pcb_table, dispatcher, base):
        self._pcbTable = pcb_table
        self._dispatcher = dispatcher
        self._base = base

    def is_empty(self):
        return self._base.is_empty()

    def add(self, pid):
        pcb_run = self._pcbTable.get_running()
        if self._pcbTable.get_priority(pid) < pcb_run['priority']:
            logger.info("PCB entrante con mayor prioridad que running!")
            self._dispatcher.save()
            self._dispatcher.load(pid)
            pcb_run['state'] = STATE_READY
            self._base.add(pcb_run['pid'])
        else:
            self._base.add(pid)

    def next(self):
        return self._base.next()


class RoundRobin:
    def __init__(self, base, quantum, timer):
        timer.start(quantum)
        self._base = base

    def is_empty(self):
        return self._base.is_empty()

    def add(self, pid):
        self._base.add(pid)

    def next(self):
        return self._base.next()


class Scheduler:
    def __init__(self, pcb_table, dispatcher, timer, tipo):
        self._pcbTable = pcb_table
        self._dispatcher = dispatcher
        self._timer = timer
        self.__tipo = tipo

    def __add(self, pid):
        self._pcbTable.set_pcb_state(pid, STATE_READY)
        self.__tipo.add(pid)

    def add_running(self):
        self.__add(self._pcbTable.get_running_pid())

    def run_or_add_queue(self, pid):
        if self._pcbTable.is_running():
            self.__add(pid)
        else:
            self._dispatcher.load(pid)

    def load_from_ready(self):
        self._pcbTable.set_running(None)
        self._timer.stop()
        if not self.__tipo.is_empty():
            self._dispatcher.load(self.__tipo.next())
