#!/usr/bin/env python

from src.log import logger
from src.interruption_handlers import STATE_READY

__all__ = ["SchedulerType", "Scheduler"]


class SchedulerType:
    @staticmethod
    def str(tipo):
        return {
            0: 'FCFS',
            1: 'Priority No Expropiativo',
            2: 'Priority Expropiativo',
            3: 'Round Robin',
            4: 'Round Robin Priority No Expropiativo',
            5: 'Round Robin Priority Expropiativo'
        }[tipo]

    @staticmethod
    def all_schedulers():
        return range(6)

    @staticmethod
    def choose():
        return int(input("\n\nTipo de Scheduler:\n"
                         + "".join(["{i} - {sch}\n".format(i=i, sch=SchedulerType.str(i))
                                    for i in SchedulerType.all_schedulers()])
                         + "Opción: "))

    @staticmethod
    def new(tipo, pcb_table, dispatcher, timer):
        if tipo == 0:
            return FCFS()
        elif tipo == 1:
            return PriorityNoExp(pcb_table)
        elif tipo == 2:
            return PriorityExp(pcb_table, dispatcher, PriorityNoExp(pcb_table))
        elif tipo == 3:
            return RoundRobin(FCFS(), 2, timer)
        elif tipo == 4:
            return RoundRobin(PriorityNoExp(pcb_table), 2, timer)
        elif tipo == 5:
            return RoundRobin(PriorityExp(pcb_table, dispatcher, PriorityNoExp(pcb_table)), 2, timer)
        else:
            raise Exception('scheduler type {sch} not recongnized'.format(sch=tipo))


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
            [self._ready[i - 1].append(self._ready[i].pop(0)) for i in range(1, self.__cant_priority) if self._ready[i]]

    def next(self):
        pid = self.__get_max_priority()
        self.__aging()
        return pid

    def add(self, pid):
        self._ready[self._pcb_table.get_priority(pid) - 1].append(pid)


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
