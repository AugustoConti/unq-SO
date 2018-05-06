#!/usr/bin/env python

from src.hardware import HARDWARE
from src.schedulers import *
from src.so import IoDeviceController, Loader, PCBTable, Dispatcher
from src.interruption_handlers import register_handlers


class Kernel:
    def __init__(self, scheduler_type):
        self._io_device_controller = IoDeviceController(HARDWARE.io_device)
        self._loader = Loader(HARDWARE.disk, HARDWARE.memory)
        self._pcb_table = PCBTable()
        self._dispatcher = Dispatcher(self._pcb_table, HARDWARE.cpu, HARDWARE.mmu, HARDWARE.timer)

        if scheduler_type == SchedulerType.fcfs():
            sch = FCFS()
        elif scheduler_type == SchedulerType.priority_no_expropiativo():
            sch = PriorityNoExp(self._pcb_table)
        elif scheduler_type == SchedulerType.priority_expropiativo():
            sch = PriorityExp(self._pcb_table, self._dispatcher, PriorityNoExp(self._pcb_table))
        elif scheduler_type == SchedulerType.round_robin():
            sch = RoundRobin(FCFS(), 2, HARDWARE.timer)
        else:
            raise Exception('scheduler type {sch} not recongnized'.format(sch=scheduler_type))

        self._scheduler = Scheduler(self._pcb_table, self._dispatcher, HARDWARE.timer, sch)

        register_handlers(self._scheduler, self._pcb_table, self._loader, self._dispatcher, self._io_device_controller,
                          HARDWARE.timer)

    def pcb_list(self):
        return self._pcb_table.pcb_list()
