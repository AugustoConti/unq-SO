#!/usr/bin/env python

from src.hardware import HARDWARE
from src.log import logger

STATE_NEW = 'NEW'
STATE_READY = 'READY'
STATE_WAITING = 'WAITING'
STATE_RUNNING = 'RUNNING'
STATE_TERMINATED = 'TERMINATED'

class KillInterruptionHandler:
    def __init__(self, scheduler, pcbTable, dispatcher):
        self._scheduler = scheduler
        self._pcbTable = pcbTable
        self._dispatcher = dispatcher

    def execute(self, irq):
        logger.info(" Finished: {currentPCB}"
                    .format(currentPCB=self._pcbTable.getRunning()))

        self._pcbTable.getRunning()['state'] = STATE_TERMINATED
        self._dispatcher.save()
        self._scheduler.loadFromReady()


class IoInInterruptionHandler:
    def __init__(self, scheduler, pcbTable, ioDeviceController, dispatcher):
        self._scheduler = scheduler
        self._pcbTable = pcbTable
        self._ioDeviceController = ioDeviceController
        self._dispatcher = dispatcher

    def execute(self, irq):
        self._pcbTable.getRunning()['state'] = STATE_WAITING
        self._dispatcher.save()
        self._ioDeviceController.runOperation(self._pcbTable.getRunningPid(), irq.parameters)
        self._scheduler.loadFromReady()


class TimeOutInterruptionHandler:
    def __init__(self, scheduler, dispatcher):
        self._scheduler = scheduler
        self._dispatcher = dispatcher
        # self._pcbTable = pcbTable

    def execute(self, irq):
        self._dispatcher.save()
        self._scheduler.addRunning()
        self._scheduler.loadFromReady()
        HARDWARE.timer.reset(True)


class NewInterruptionHandler:
    def __init__(self, scheduler, pcbTable, loader):
        self._scheduler = scheduler
        self._pcbTable = pcbTable
        self._loader = loader

    def execute(self, irq):
        program = irq.parameters['program']
        pcb = {'pid': self._pcbTable.getPID(),
               'priority': irq.parameters['priority'],
               'name': program,
               'pc': 0,
               'state': STATE_NEW}
        self._loader.load(pcb, program)

        self._pcbTable.addPCB(pcb)
        self._scheduler.runOrAddQueue(pcb['pid'])
        logger.info(HARDWARE)


class IoOutInterruptionHandler:
    def __init__(self, scheduler, ioDeviceController):
        self._scheduler = scheduler
        self._ioDeviceController = ioDeviceController

    def execute(self, irq):
        self._scheduler.runOrAddQueue(self._ioDeviceController.getFinishedPid())
        logger.info(self._ioDeviceController)