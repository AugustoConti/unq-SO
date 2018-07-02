from tabulate import tabulate

from src.utils.log import logger
from src.structures.states import State


class Preemptive:
    def __init__(self, pcb_table, dispatcher):
        self._pcbTable = pcb_table
        self._dispatcher = dispatcher

    def add(self, pid, comparer):
        pid_run = self._pcbTable.get_running_pid()
        if comparer(pid) < comparer(pid_run):
            logger.info("Preemptive", "Realizando context switching")
            self._dispatcher.save(State.READY)
            self._dispatcher.load(pid)
            return pid_run
        else:
            return pid


class SJF:
    def __init__(self, pcb_table, preemptive):
        self._pcbTable = pcb_table
        self._preemptive = preemptive
        self._ready = []

    def is_empty(self):
        return not self._ready

    def add(self, pid):
        self._ready.append(self._preemptive.add(pid, self._pcbTable.get_intructions_left))

    def next(self):
        minimo = sorted(self._ready, key=lambda pid: self._pcbTable.get_intructions_left(pid))[0]
        self._ready.remove(minimo)
        return minimo

    def kill(self, pid):
        if pid in self._ready:
            self._ready.remove(pid)

    def __repr__(self):
        return 'SJF: {ready}'.format(ready=self._ready)


class FCFS:
    def __init__(self):
        self._ready = []

    def is_empty(self):
        return not self._ready

    def add(self, pid):
        self._ready.append(pid)

    def next(self):
        return self._ready.pop(0)

    def kill(self, pid):
        if pid in self._ready:
            self._ready.remove(pid)

    def __repr__(self):
        return 'FCFS: {ready}'.format(ready=self._ready)


class PriorityNoPreemptive:
    def __init__(self, pcb_table):
        self.__cant = 5
        self.__doAging = 0
        self._pcb_table = pcb_table
        self._ready = [[] for _ in range(self.__cant)]

    def is_empty(self):
        return not any(self._ready)

    def __get_max_priority(self):
        for plist in self._ready:
            if plist:
                return plist.pop(0)

    def __aging(self):
        self.__doAging += 1
        if self.__doAging % 4 == 0:
            logger.info('PriorityNoPreemptive', 'Doing aging!')
            [self._ready[i - 1].append(self._ready[i].pop(0)) for i in range(1, self.__cant) if self._ready[i]]

    def next(self):
        pid = self.__get_max_priority()
        self.__aging()
        return pid

    def add(self, pid):
        self._ready[self._pcb_table.get_priority(pid) - 1].append(pid)

    def kill(self, pid):
        [self._ready[i].remove(pid) for i in range(self.__cant) if pid in self._ready[i]]

    def __repr__(self):
        return 'PriorityNoPreemptive:\n{ready}'.format(
            ready=tabulate(self._ready, tablefmt='grid'))


class PriorityPreemptive:
    def __init__(self, pcb_table, preemptive, base):
        self._pcbTable = pcb_table
        self._preemptive = preemptive
        self._base = base

    def is_empty(self):
        return self._base.is_empty()

    def add(self, pid):
        self._base.add(self._preemptive.add(pid, self._pcbTable.get_priority))

    def next(self):
        return self._base.next()

    def kill(self, pid):
        self._base.kill(pid)

    def __repr__(self):
        return 'PriorityPreemptive: {ready}'.format(ready=self._base)


class RoundRobin:
    def __init__(self, base, timer, quantum):
        self._base = base
        timer.start(quantum)

    def is_empty(self):
        return self._base.is_empty()

    def add(self, pid):
        self._base.add(pid)

    def next(self):
        return self._base.next()

    def kill(self, pid):
        self._base.kill(pid)

    def __repr__(self):
        return 'RoundRobin: {ready}'.format(ready=self._base)
