from src.so.schedulers_types import *


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
        return int(input("\n\nType Scheduler:\n"
                         + "".join(["{i} - {sch}\n".format(i=i, sch=SchedulerType.str(i))
                                    for i in SchedulerType.all_schedulers()])
                         + "Choice: "))

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
