from src.log import logger


class DispatcherBasic:
    def __init__(self, mmu):
        self._mmu = mmu

    def load(self, pcb):
        self._mmu.set_base_dir(pcb['baseDir'])
        self._mmu.set_limit(pcb['limit'])


class DispatcherPaged:
    def __init__(self, mm, mmu):
        self._mmu = mmu
        self._mm = mm

    def load(self, pcb):
        self._mmu.set_page_table(self._mm.get_page_table(pcb['pid']))


class Dispatcher:
    def __init__(self, base, pcb_table, cpu, timer):
        self._base = base
        self._pcb_table = pcb_table
        self._cpu = cpu
        self._timer = timer

    def save(self):
        self._pcb_table.get_running()['pc'] = self._cpu.get_pc()
        self._cpu.set_pc(-1)

    def load(self, pid):
        pcb = self._pcb_table.set_running(pid)
        self._base.load(pcb)
        self._cpu.set_pc(pcb['pc'])
        self._timer.reset()
        logger.info(" CPU running: {currentPCB}".format(currentPCB=pcb))
