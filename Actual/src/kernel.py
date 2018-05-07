#!/usr/bin/env python

from src.schedulers import *
from src.so import IoDeviceController, Loader, PCBTable, Dispatcher
from src.interruption_handlers import register_handlers


class Kernel:
    def __init__(self, hardware, scheduler_type):
        self._io_device_controller = IoDeviceController(hardware.io_device())
        self._loader = Loader(hardware.disk(), hardware.memory())
        self._pcb_table = PCBTable()
        self._dispatcher = Dispatcher(self._pcb_table, hardware.cpu(), hardware.mmu(), hardware.timer())

        if scheduler_type == SchedulerType.fcfs():
            sch = FCFS()
        elif scheduler_type == SchedulerType.priority_no_expropiativo():
            sch = PriorityNoExp(self._pcb_table)
        elif scheduler_type == SchedulerType.priority_expropiativo():
            sch = PriorityExp(self._pcb_table, self._dispatcher, PriorityNoExp(self._pcb_table))
        elif scheduler_type == SchedulerType.round_robin():
            sch = RoundRobin(FCFS(), 2, hardware.timer())
        else:
            raise Exception('scheduler type {sch} not recongnized'.format(sch=scheduler_type))

        self._scheduler = Scheduler(self._pcb_table, self._dispatcher, hardware.timer(), sch)

        register_handlers(hardware.interrupt_vector(), self._scheduler, self._pcb_table, self._loader, self._dispatcher,
                          self._io_device_controller, hardware.timer())

    def pcb_list(self):
        return self._pcb_table.pcb_list()
