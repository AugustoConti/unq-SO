from src.hardware.mmu import MMU
from src.hardware.mmu_types import MMUBasic, MMUPaged
from src.system.dispatcher import DispatcherBasic, DispatcherPaged, Dispatcher
from src.system.loader import LoaderBasic, LoaderPagedBase, LoaderPaged, LoaderPagedOnDemand
from src.system.memory_manager.memory_manager import MemoryManagerPaged, MemoryManagerPagedOnDemand


class Meta(type):
    def __str__(self):
        return getattr(self, '_class_repr')()


class AsignacionContinuaFactory(metaclass=Meta):
    @classmethod
    def _class_repr(cls):
        return 'Asignación Continua'

    @staticmethod
    def is_on_demand():
        return False

    @staticmethod
    def new_mmu(memory, frame_size, interrupt_vector):
        return MMU(MMUBasic(memory))

    @staticmethod
    def new_loader(disk, memory, mm, frame_size, swap):
        return LoaderBasic(disk, memory)

    @staticmethod
    def new_dispatcher(mm, mmu, pcb_table, cpu, timer):
        return Dispatcher(DispatcherBasic(mmu), pcb_table, cpu, timer)

    @staticmethod
    def new_memory_manager(loader, swap, algorithm):
        return MemoryManagerPaged()


class PagedFactory(metaclass=Meta):
    @classmethod
    def _class_repr(cls):
        return 'Paginación'

    @staticmethod
    def is_on_demand():
        return False

    @staticmethod
    def new_mmu(memory, frame_size, interrupt_vector):
        return MMU(MMUPaged(memory, interrupt_vector, frame_size))

    @staticmethod
    def new_loader(disk, memory, mm, frame_size, swap):
        return LoaderPagedBase(LoaderPaged(mm), disk, swap, memory, mm, frame_size)

    @staticmethod
    def new_dispatcher(mm, mmu, pcb_table, cpu, timer):
        return Dispatcher(DispatcherPaged(mm, mmu), pcb_table, cpu, timer)

    @staticmethod
    def new_memory_manager(loader, swap, algorithm):
        return MemoryManagerPaged()


class PagedOnDemandFactory(metaclass=Meta):
    @classmethod
    def _class_repr(cls):
        return 'Paginación bajo demanda'

    @staticmethod
    def is_on_demand():
        return True

    @staticmethod
    def new_mmu(memory, frame_size, interrupt_vector):
        return MMU(MMUPaged(memory, interrupt_vector, frame_size))

    @staticmethod
    def new_loader(disk, memory, mm, frame_size, swap):
        return LoaderPagedBase(LoaderPagedOnDemand(), disk, swap, memory, mm, frame_size)

    @staticmethod
    def new_dispatcher(mm, mmu, pcb_table, cpu, timer):
        return Dispatcher(DispatcherPaged(mm, mmu), pcb_table, cpu, timer)

    @staticmethod
    def new_memory_manager(loader, swap, algorithm):
        return MemoryManagerPagedOnDemand(algorithm, loader, swap)
