from src.menu import selection_menu
from src.system.schedulers import Scheduler
from src.system.schedulers_types import *


class SchedulerType:
    lista = ['Shorter Job First',
             'FCFS',
             'Priority No Preemptive',
             'Priority Preemptive',
             'Round Robin',
             'Round Robin Priority No Preemptive',
             'Round Robin Priority Preemptive']

    @staticmethod
    def is_rr(tipo):
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
