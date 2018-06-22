from src.system.schedulers_types import *
from src.system.states import State
from src.menu import selection_menu


class SchedulerType:
    lista = ['Shorter Job First',
             'FCFS',
             'Priority No Preemptive',
             'Priority Preemptive',
             'Round Robin',
             'Round Robin Priority No Preemptive',
             'Round Robin Priority Preemptive']

    @staticmethod
    def str(tipo):
        return SchedulerType.lista[tipo]

    @staticmethod
    def all():
        return range(len(SchedulerType.lista))

    @staticmethod
    def choose():
        return selection_menu(SchedulerType.lista, "Scheduler Type")

    @staticmethod
    def new(tipo, pcb_table, dispatcher, timer):
        if tipo == 0:
            return SJF(pcb_table, Preemptive(pcb_table, dispatcher))
        elif tipo == 1:
            return FCFS()
        elif tipo == 2:
            return PriorityNoPreemptive(pcb_table)
        elif tipo == 3:
            return PriorityPreemptive(pcb_table, Preemptive(pcb_table, dispatcher), PriorityNoPreemptive(pcb_table))
        elif tipo == 4:
            return RoundRobin(FCFS(), 2, timer)
        elif tipo == 5:
            return RoundRobin(PriorityNoPreemptive(pcb_table), 2, timer)
        elif tipo == 6:
            return RoundRobin(
                PriorityPreemptive(pcb_table, Preemptive(pcb_table, dispatcher), PriorityNoPreemptive(pcb_table)), 2,
                timer)
        else:
            raise Exception('Scheduler type {sch} not recongnized'.format(sch=tipo))


class Scheduler:
    def __init__(self, pcb_table, dispatcher, timer, tipo):
        self._pcbTable = pcb_table
        self._dispatcher = dispatcher
        self._timer = timer
        self.__tipo = tipo

    def __add(self, pid):
        self._pcbTable.set_pcb_state(pid, State.READY)
        self.__tipo.add(pid)

    def add_running_and_load(self):
        self.__add(self._pcbTable.get_running_pid())
        self.load_from_ready()

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
