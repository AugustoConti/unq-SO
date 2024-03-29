from src.log import logger
from src.structures.interruptions import Interruption
from src.structures.states import State


class KillInterruptionHandler:
    def __init__(self, scheduler, pcb_table, dispatcher, mm):
        self._scheduler = scheduler
        self._pcbTable = pcb_table
        self._dispatcher = dispatcher
        self._mm = mm

    def execute(self, irq):
        logger.info(" Finished: {currentPCB}".format(currentPCB=self._pcbTable.get_running()))
        running = self._pcbTable.get_running_pid()
        self._mm.kill(running)
        self._pcbTable.set_pcb_state(running, State.TERMINATED)
        self._dispatcher.save()
        self._scheduler.load_from_ready()


class IoInInterruptionHandler:
    def __init__(self, scheduler, pcb_table, io_device_controller, dispatcher):
        self._scheduler = scheduler
        self._pcbTable = pcb_table
        self._ioDeviceController = io_device_controller
        self._dispatcher = dispatcher

    def execute(self, irq):
        self._pcbTable.set_pcb_state(self._pcbTable.get_running_pid(), State.WAITING)
        self._dispatcher.save()
        self._ioDeviceController.run_operation(self._pcbTable.get_running_pid(), irq.parameters())
        self._scheduler.load_from_ready()


class TimeOutInterruptionHandler:
    def __init__(self, scheduler, dispatcher, timer):
        self._scheduler = scheduler
        self._dispatcher = dispatcher
        self._timer = timer

    def execute(self, irq):
        logger.info("TimeOut Interruption")
        self._dispatcher.save()
        self._scheduler.add_running()
        self._scheduler.load_from_ready()
        self._timer.reset(True)


class NewInterruptionHandler:
    def __init__(self, scheduler, pcb_table, loader):
        self._scheduler = scheduler
        self._pcbTable = pcb_table
        self._loader = loader

    def execute(self, irq):
        pcb = {'pid': self._pcbTable.get_pid(),
               'priority': irq.parameters()['priority'],
               'name': irq.parameters()['program'],
               'pc': 0,
               'state': State.NEW}
        self._loader.load(pcb)
        self._pcbTable.add_pcb(pcb)
        self._scheduler.run_or_add_queue(pcb['pid'])


class IoOutInterruptionHandler:
    def __init__(self, scheduler, io_device_controller):
        self._scheduler = scheduler
        self._io_device_controller = io_device_controller

    def execute(self, irq):
        self._scheduler.run_or_add_queue(self._io_device_controller.get_finished_pid())
        logger.info(self._io_device_controller)


class PageFaultInterruptionHandler:
    def __init__(self, mm, pcb_table, loader, mmu):
        self._mm = mm
        self._pcbTable = pcb_table
        self._loader = loader
        self._mmu = mmu

    def execute(self, irq):
        run = self._pcbTable.get_running_pid()
        self._mm.add_page_table(run, self._mmu.get_page_table())
        page = irq.parameters()
        frame = self._mm.get_frame()
        idx = self._mm.get_swap_index(run, page)
        if idx == -1:
            self._loader.load_page(self._pcbTable.get_running()['name'], page, frame)
        else:
            self._loader.swap_out(idx, frame)
        self._mm.update_page(run, page, frame)
        self._mmu.set_page_table(self._mm.get_page_table(run))


def register_handlers(interrupt_vector, scheduler, pcb_table, loader, dispatcher, io_device_controller, timer, mm, mmu):
    interrupt_vector.register(Interruption.NEW,
                              NewInterruptionHandler(scheduler, pcb_table, loader))
    interrupt_vector.register(Interruption.KILL,
                              KillInterruptionHandler(scheduler, pcb_table, dispatcher, mm))
    interrupt_vector.register(Interruption.IO_IN,
                              IoInInterruptionHandler(scheduler, pcb_table, io_device_controller, dispatcher))
    interrupt_vector.register(Interruption.IO_OUT,
                              IoOutInterruptionHandler(scheduler, io_device_controller))
    interrupt_vector.register(Interruption.TIME_OUT,
                              TimeOutInterruptionHandler(scheduler, dispatcher, timer))
    interrupt_vector.register(Interruption.PAGE_FAULT,
                              PageFaultInterruptionHandler(mm, pcb_table, loader, mmu))
