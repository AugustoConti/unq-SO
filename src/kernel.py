#!/usr/bin/env python

from src.schedulers import *
from src.so import IoDeviceController, Loader, LoaderBasic, PCBTable, Dispatcher, DispatcherBasic, MemoryManager
from src.interruption_handlers import register_handlers


class Kernel:
    def __init__(self, hardware, scheduler_tipo):
        self._mm = MemoryManager(4)
        self._io_device_controller = IoDeviceController(hardware.io_device())
        self._loader = Loader(LoaderBasic(hardware.memory()), hardware.disk())
        self._pcb_table = PCBTable()
        self._dispatcher = Dispatcher(DispatcherBasic(hardware.mmu()), self._pcb_table, hardware.cpu(), hardware.timer())
        self._scheduler = Scheduler(self._pcb_table, self._dispatcher, hardware.timer(),
                                    SchedulerType.new(scheduler_tipo, self._pcb_table, self._dispatcher,
                                                      hardware.timer()))

        register_handlers(hardware.interrupt_vector(), self._scheduler, self._pcb_table, self._loader, self._dispatcher,
                          self._io_device_controller, hardware.timer(), self._mm)

    def pcb_list(self):
        return self._pcb_table.pcb_list()
