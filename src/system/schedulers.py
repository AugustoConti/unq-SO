from src.system.schedulers_types import *


class Scheduler:
    def __init__(self, pcb_table, dispatcher, timer, tipo):
        self._pcbTable = pcb_table
        self._dispatcher = dispatcher
        self._timer = timer
        self.__tipo = tipo

    def __add(self, pid):
        self._pcbTable.set_pcb_state(pid, State.READY)
        self.__tipo.add(pid)

    def add_running_and_load(self):
        self.__add(self._pcbTable.get_running_pid())
        self.load_from_ready()

    def run_or_add_queue(self, pid):
        if self._pcbTable.is_running():
            self.__add(pid)
        else:
            self._dispatcher.load(pid)

    def load_from_ready(self):
        self._pcbTable.set_running(None)
        self._timer.stop()
        if self.__tipo.is_empty():
            logger.info('Scheduler', 'Ready: Empty')
        else:
            logger.info('Scheduler', self.__tipo)
            self._dispatcher.load(self.__tipo.next())
