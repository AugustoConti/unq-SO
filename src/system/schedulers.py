from src.menu import selection_menu
from src.system.schedulers_types import *
from src.system.states import State


class SchedulerType:
    lista = ['Shorter Job First',
             'FCFS',
             'Priority No Preemptive',
             'Priority Preemptive',
             'Round Robin',
             'Round Robin Priority No Preemptive',
             'Round Robin Priority Preemptive']

    @staticmethod
    def isRR(tipo):
        return tipo in [4, 5, 6]

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
    def new(tipo, pcb_table, dispatcher, timer, quantum):
        if tipo == 0:
            sch = SJF(pcb_table, Preemptive(pcb_table, dispatcher))
        elif tipo == 1:
            sch = FCFS()
        elif tipo == 2:
            sch = PriorityNoPreemptive(pcb_table)
        elif tipo == 3:
            sch = PriorityPreemptive(pcb_table, Preemptive(pcb_table, dispatcher), PriorityNoPreemptive(pcb_table))
        elif tipo == 4:
            sch = RoundRobin(FCFS(), timer, quantum)
        elif tipo == 5:
            sch = RoundRobin(PriorityNoPreemptive(pcb_table), timer, quantum)
        elif tipo == 6:
            sch = RoundRobin(PriorityPreemptive(pcb_table, Preemptive(pcb_table, dispatcher),
                                                PriorityNoPreemptive(pcb_table)), timer, quantum)
        else:
            raise Exception('Scheduler type {sch} not recongnized'.format(sch=tipo))
        return Scheduler(pcb_table, dispatcher, timer, sch)


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
        if self.__tipo.is_empty():
            logger.info('Scheduler', 'Ready: Empty')
        else:
            logger.info('Scheduler', self.__tipo)
            self._dispatcher.load(self.__tipo.next())
