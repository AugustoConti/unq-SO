#!/usr/bin/env python

from src.schedulers import *
from src.mmu import *
from src.so import IoDeviceController, Loader, PCBTable, Dispatcher, MemoryManager
from src.interruption_handlers import register_handlers

# TODO pcb_list de pcb_table, crear en variable de kernel y pasar por param en constructor de pcb_table
class Kernel:
    def __init__(self, hardware, scheduler_type, mmu_type, frame_size):
        self._mm = MemoryManager(4)
        self._io_device_controller = IoDeviceController(hardware.io_device())
        self._pcb_table = PCBTable()
        self._loader = Loader(MMUType.new_loader(mmu_type, hardware.memory(), self._mm, frame_size), hardware.disk())
        self._dispatcher = Dispatcher(MMUType.new_dispatcher(mmu_type, self._mm, hardware.mmu()), self._pcb_table,
                                      hardware.cpu(), hardware.timer())
        self._scheduler = Scheduler(self._pcb_table, self._dispatcher, hardware.timer(),
                                    SchedulerType.new(scheduler_type, self._pcb_table, self._dispatcher, hardware.timer()))
        register_handlers(hardware.interrupt_vector(), self._scheduler, self._pcb_table, self._loader, self._dispatcher,
                          self._io_device_controller, hardware.timer(), self._mm)

    def pcb_list(self):
        return self._pcb_table.pcb_list()
