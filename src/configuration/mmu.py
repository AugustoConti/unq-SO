from src.hardware.mmu import MMU
from src.hardware.mmu_types import MMUBasic, MMUPaged
from src.menu import selection_menu
from src.system.dispatcher import DispatcherBasic, DispatcherPaged, Dispatcher
from src.system.loader import LoaderBasic, LoaderPagedBase, LoaderPaged, LoaderPagedOnDemand
from src.system.memory_manager.memory_manager import MemoryManagerPaged, MemoryManagerPagedOnDemand


class MMUType:
    lista = ['Asignación Continua', 'Paginación', 'Paginación bajo demanda']

    @staticmethod
    def is_on_demand(tipo):
        return tipo == 2

    @staticmethod
    def str(tipo):
        return MMUType.lista[tipo]

    @staticmethod
    def all():
        return range(len(MMUType.lista))

    @staticmethod
    def choose():
        return selection_menu(MMUType.lista, "MMU Type")

    @staticmethod
    def new_mmu(tipo, memory, frame_size, interrupt_vector):
        if tipo == 0:
            mmu = MMUBasic(memory)
        elif tipo in [1, 2]:
            mmu = MMUPaged(memory, interrupt_vector, frame_size)
        else:
            raise Exception('MMU type {mmu} not recongnized'.format(mmu=tipo))
        return MMU(mmu)

    @staticmethod
    def new_loader(tipo, disk, memory, mm, frame_size, swap):
        if tipo == 0:
            return LoaderBasic(disk, memory)
        elif tipo == 1:
            return LoaderPagedBase(LoaderPaged(mm), disk, swap, memory, mm, frame_size)
        elif tipo == 2:
            return LoaderPagedBase(LoaderPagedOnDemand(), disk, swap, memory, mm, frame_size)
        else:
            raise Exception('Loader type {loader} not recongnized'.format(loader=tipo))

    @staticmethod
    def new_dispatcher(tipo, mm, mmu, pcb_table, cpu, timer):
        if tipo == 0:
            disp = DispatcherBasic(mmu)
        elif tipo in [1, 2]:
            disp = DispatcherPaged(mm, mmu)
        else:
            raise Exception('Dispatcher type {dispatcher} not recongnized'.format(dispatcher=tipo))
        return Dispatcher(disp, pcb_table, cpu, timer)

    @staticmethod
    def new_memory_manager(tipo, loader, swap, algorithm):
        if tipo in [0, 1]:
            return MemoryManagerPaged()
        elif tipo == 2:
            return MemoryManagerPagedOnDemand(algorithm, loader, swap)
        else:
            raise Exception('Memory Manager type {mm} not recongnized'.format(mm=tipo))
