from src.log import logger
from src.hardware.hardware import NEW_INTERRUPTION_TYPE, KILL_INTERRUPTION_TYPE, IO_IN_INTERRUPTION_TYPE, IO_OUT_INTERRUPTION_TYPE, TIME_OUT_INTERRUPTION_TYPE

STATE_NEW = 'NEW'
STATE_READY = 'READY'
STATE_WAITING = 'WAITING'
STATE_RUNNING = 'RUNNING'
STATE_TERMINATED = 'TERMINATED'


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
        self._pcbTable.set_pcb_state(running, STATE_TERMINATED)
        self._dispatcher.save()
        self._scheduler.load_from_ready()


class IoInInterruptionHandler:
    def __init__(self, scheduler, pcb_table, io_device_controller, dispatcher):
        self._scheduler = scheduler
        self._pcbTable = pcb_table
        self._ioDeviceController = io_device_controller
        self._dispatcher = dispatcher

    def execute(self, irq):
        self._pcbTable.set_pcb_state(self._pcbTable.get_running_pid(), STATE_WAITING)
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
               'state': STATE_NEW}
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


def register_handlers(interrupt_vector, scheduler, pcb_table, loader, dispatcher, io_device_controller, timer, mm):
    interrupt_vector.register(NEW_INTERRUPTION_TYPE,
                              NewInterruptionHandler(scheduler, pcb_table, loader))
    interrupt_vector.register(KILL_INTERRUPTION_TYPE,
                              KillInterruptionHandler(scheduler, pcb_table, dispatcher, mm))
    interrupt_vector.register(IO_IN_INTERRUPTION_TYPE,
                              IoInInterruptionHandler(scheduler, pcb_table, io_device_controller, dispatcher))
    interrupt_vector.register(IO_OUT_INTERRUPTION_TYPE,
                              IoOutInterruptionHandler(scheduler, io_device_controller))
    interrupt_vector.register(TIME_OUT_INTERRUPTION_TYPE,
                              TimeOutInterruptionHandler(scheduler, dispatcher, timer))
