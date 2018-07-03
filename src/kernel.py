from src.configuration.scheduler import SchedulerType
from src.system.interruption_handlers import register_handlers
from src.system.io_device_controller import IoDeviceController, ControllerDevices
from src.system.memory_manager.memory_manager import MemoryManager
from src.system.pcb_table import PCBTable


class Kernel:
    def __init__(self, hard, scheduler_type, mmu_type, frame_size, count_frames, quantum, algorithm):
        self._scheduler_type = scheduler_type
        self._mmu_type = mmu_type
        self._count_frames = count_frames
        self._quantum = quantum
        self._table = dict()
        self._mm = MemoryManager(count_frames)
        self._pcb_table = PCBTable(self._table)
        self._loader = mmu_type.new_loader(hard.disk(), hard.memory(), self._mm, frame_size, hard.swap())
        self._mm.set_base(mmu_type.new_mm(self._loader, hard.swap(), algorithm))
        self._dispatcher = mmu_type.new_dispatcher(self._mm, hard.mmu(), self._pcb_table, hard.cpu(), hard.timer())
        self._scheduler = SchedulerType.new(scheduler_type, self._pcb_table, self._dispatcher, hard.timer(), quantum)

        devices = {}
        for d in hard.io_devices():
            devices[d.device_id()] = IoDeviceController(d)

        register_handlers(hard.interrupt_vector(), self._scheduler, self._pcb_table, self._loader, self._dispatcher,
                          ControllerDevices(devices), hard.timer(), self._mm, hard.mmu())

    def info(self):
        return [['Cantidad de Frames', self._count_frames],
                ['MMU', self._mmu_type],
                ['Scheduler', SchedulerType.str(self._scheduler_type)],
                ['Quantum', self._quantum]]

    def mem_info(self):
        return self._loader.get_info()

    def contains_pid(self, pid):
        return self._pcb_table.contains_pid(pid)

    def pcb_list(self):
        return self._table.values()

    def page_table(self):
        return self._mm.page_table()
