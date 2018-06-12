from src.system.schedulers import *
from src.hardware.mmu import *
from src.system.so import IoDeviceController, PCBTable
from src.system.dispatcher import Dispatcher
from src.system.interruption_handlers import register_handlers


class Kernel:
    def __init__(self, hardware, scheduler_type, mmu_type, frame_size, count_frames):
        self._table = dict()
        self._mm = MemoryManager(count_frames)
        self._io_device_controller = IoDeviceController(hardware.io_device())
        self._pcb_table = PCBTable(self._table)
        self._loader = MMUType.new_loader(mmu_type, hardware.disk(), hardware.memory(), self._mm, frame_size,
                                          hardware.swap())
        self._mm.set_base(MMUType.new_memory_manager(mmu_type, self._loader, hardware.swap()))
        self._dispatcher = Dispatcher(MMUType.new_dispatcher(mmu_type, self._mm, hardware.mmu()), self._pcb_table,
                                      hardware.cpu(), hardware.timer())
        self._scheduler = Scheduler(self._pcb_table, self._dispatcher, hardware.timer(),
                                    SchedulerType.new(scheduler_type, self._pcb_table, self._dispatcher,
                                                      hardware.timer()))
        register_handlers(hardware.interrupt_vector(), self._scheduler, self._pcb_table, self._loader, self._dispatcher,
                          self._io_device_controller, hardware.timer(), self._mm, hardware.mmu())

    def pcb_list(self):
        return self._table.values()
