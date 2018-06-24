from src.hardware.mmu import *
from src.system.dispatcher import Dispatcher
from src.system.interruption_handlers import register_handlers
from src.system.io_device_controller import IoDeviceController
from src.system.pcb_table import PCBTable
from src.system.schedulers import *


class Kernel:
    def __init__(self, hardware, scheduler_type, mmu_type, frame_size, count_frames, quantum, algorithm):
        self._scheduler_type = scheduler_type
        self._mmu_type = mmu_type
        self._count_frames = count_frames
        self._quantum = quantum
        self._table = dict()
        self._mm = MemoryManager(count_frames)
        self._pcb_table = PCBTable(self._table)
        self._io_device_controller = IoDeviceController(hardware.io_device())
        self._loader = MMUType.new_loader(mmu_type, hardware.disk(), hardware.memory(), self._mm, frame_size,
                                          hardware.swap())
        self._mm.set_base(MMUType.new_memory_manager(mmu_type, self._loader, hardware.swap(), algorithm))
        self._dispatcher = Dispatcher(MMUType.new_dispatcher(mmu_type, self._mm, hardware.mmu()), self._pcb_table,
                                      hardware.cpu(), hardware.timer())
        self._scheduler = SchedulerType.new(scheduler_type, self._pcb_table, self._dispatcher, hardware.timer(),
                                            quantum)
        register_handlers(hardware.interrupt_vector(), self._scheduler, self._pcb_table, self._loader, self._dispatcher,
                          self._io_device_controller, hardware.timer(), self._mm, hardware.mmu())

    def info(self):
        return [['Cantidad de Frames', self._count_frames],
                ['MMU', MMUType.str(self._mmu_type)],
                ['Scheduler', SchedulerType.str(self._scheduler_type)]] \
               + ([['Quantum', self._quantum]] if SchedulerType.isRR(self._scheduler_type) else [])

    def pcb_list(self):
        return self._table.values()
