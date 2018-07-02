from src.configuration.mmu_factory import AsignacionContinuaFactory, PagedFactory, PagedOnDemandFactory
from src.utils.menu import selection_menu


class MMUType:
    lista = [AsignacionContinuaFactory, PagedFactory, PagedOnDemandFactory]

    @staticmethod
    def choose():
        return MMUType.lista[selection_menu(MMUType.lista, "MMU Type")]
