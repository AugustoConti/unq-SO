#!/usr/bin/env python

# return A+1 if A > B else A-1

from hardware import *
from log import logger


def execute(program, priority=3):
    HARDWARE.interruptVector.handle(IRQ(NEW_INTERRUPTION_TYPE, {'program': program, 'priority': priority}))


def expand(instructions):
    expanded = []
    for i in instructions:
        if isinstance(i, list):
            expanded.extend(i)
        else:
            expanded.append(i)
    if not ASM.isEXIT(expanded[-1]):
        expanded.append(INSTRUCTION_EXIT)
    return expanded


class IoDeviceController:
    def __init__(self, device):
        self._device = device
        self._waiting_queue = []
        self._currentPid = None

    @property
    def isBusy(self):
        return self._device.is_busy or self._waiting_queue

    def runOperation(self, pid, instruction):
        pair = {'pid': pid, 'instruction': instruction}
        self._waiting_queue.append(pair)
        self.__load_from_waiting_queue_if_apply()
        logger.info(self)

    def getFinishedPid(self):
        finishedPid = self._currentPid
        self._currentPid = None
        self.__load_from_waiting_queue_if_apply()
        return finishedPid

    def __load(self, pair):
        print(pair)
        self._currentPid = pair['pid']
        self._device.execute(pair['instruction'])

    def __load_from_waiting_queue_if_apply(self):
        if self._waiting_queue and self._device.is_idle:
            self.__load(self._waiting_queue.pop(0))

    def __repr__(self):
        return "IoDeviceController for {deviceID} running: {currentPid} waiting: {waiting_queue}" \
            .format(deviceID=self._device.deviceId, currentPid=self._currentPid, waiting_queue=self._waiting_queue)


class Dispatcher:
    def __init__(self, pcbTable):
        self._pcbTable = pcbTable

    def save(self):
        self._pcbTable.getRunning()['pc'] = HARDWARE.cpu.pc
        HARDWARE.cpu.pc = -1

    def load(self, pid):
        self._pcbTable.setRunning(pid)
        pcb = self._pcbTable.getRunning()
        HARDWARE.mmu.baseDir = pcb['baseDir']
        HARDWARE.mmu.limit = pcb['limit']
        HARDWARE.cpu.pc = pcb['pc']
        HARDWARE.timer.reset()
        logger.info(" CPU running: {currentPCB}".format(currentPCB=pcb))


class Loader:
    def __init__(self):
        self._nextDir = 0

    def load(self, pcb, program):
        instructions = HARDWARE.disk.get(program)
        progSize = len(instructions)
        pcb['baseDir'] = self._nextDir
        pcb['limit'] = progSize
        for i in range(0, progSize):
            HARDWARE.memory.put(self._nextDir + i, instructions[i])
        self._nextDir += progSize


class PCBTable:
    def __init__(self):
        self._lastID = 0
        self._tabla = dict()
        self._pidRunning = None

    def getPID(self):
        self._lastID += 1
        return self._lastID

    def isRunning(self):
        return self._pidRunning is not None

    def getRunning(self):
        return self._tabla[self._pidRunning] if self.isRunning else None

    def setRunning(self, pid):
        self._pidRunning = pid

    def addPCB(self, pcb):
        self._tabla[pcb['pid']] = pcb

    def getPriority(self, pid):
        return self._tabla[pid]['priority']


class KillInterruptionHandler:
    def __init__(self, scheduler, pcbTable, dispatcher):
        self._scheduler = scheduler
        self._pcbTable = pcbTable
        self._dispatcher = dispatcher

    def execute(self, irq):
        logger.info(" Finished: {currentPCB}"
                    .format(currentPCB=self._pcbTable.getRunning()))

        self._dispatcher.save()
        self._scheduler.loadFromReady()


class IoInInterruptionHandler:
    def __init__(self, scheduler, pcbTable, ioDeviceController, dispatcher):
        self._scheduler = scheduler
        self._pcbTable = pcbTable
        self._ioDeviceController = ioDeviceController
        self._dispatcher = dispatcher

    def execute(self, irq):
        self._dispatcher.save()
        self._ioDeviceController.runOperation(self._pcbTable.getRunning()['pid'], irq.parameters)
        self._scheduler.loadFromReady()


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
               'pc': 0}
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


class TimeOutInterruptionHandler:
    def __init__(self, scheduler, dispatcher):
        self._scheduler = scheduler
        self._dispatcher = dispatcher
        # self._pcbTable = pcbTable

    def execute(self, irq):
        self._dispatcher.save()
        self._scheduler.addRunning()
        self._scheduler.loadFromReady()


class FCFS:
    def __init__(self):
        self._ready = []

    def isEmpty(self):
        return not self._ready

    def add(self, pid):
        self._ready.append(pid)

    def next(self):
        return self._ready.pop(0)


class PriorityNoExp:
    def __init__(self, pcbTable):
        self._pcbTable = pcbTable
        self._ready = []
        for i in range(5):
            self._ready.append([])

    def isEmpty(self):
        for list in self._ready:
            if list:
                return False
        return True

    def __getMaxPriority(self):
        for list in self._ready:
            if list:
                return list.pop(0)

    def __aging(self):
        for i in range(1, 4):
            if self._ready[i]:
                self._ready[i-1].append(self._ready[i].pop(0))

    def next(self):
        pid = self.__getMaxPriority()
        self.__aging()
        return pid

    def add(self, pid):
        self._ready[self._pcbTable.getPriority(pid)-1].append(pid)


class PriorityExp:
    def __init__(self, pcbTable, dispatcher, base):
        self._pcbTable = pcbTable
        self._dispatcher = dispatcher
        self._base = base

    def isEmpty(self):
        return self._base.isEmpty()

    def add(self, pid):
        pcbRun = self._pcbTable.getRunning()
        if self._pcbTable.getPriority(pid) < pcbRun['priority']:
            self._dispatcher.save()
            self._dispatcher.load(pid)
            self._base.add(pcbRun['pid'])
            logger.info("PCB entrante con mayor prioridad que running!")
        else:
            self._base.add(pid)

    def next(self):
        return self._base.next()


class RoundRobin:
    def __init__(self, base, quantum):
        HARDWARE.timer.start(quantum)
        self._base = base

    def isEmpty(self):
        return self._base.isEmpty()

    def add(self, pid):
        self._base.add(pid)

    def next(self):
        return self._base.next()


class Scheduler:
    def __init__(self, pcbTable, dispatcher, tipo):
        self.__tipo = tipo
        self._pcbTable = pcbTable
        self._dispatcher = dispatcher

    def addRunning(self):
        self.__tipo.add(self._pcbTable.getRunning()['pid'])

    def runOrAddQueue(self, pid):
        if self._pcbTable.isRunning():
            self.__tipo.add(pid)
        else:
            self._dispatcher.load(pid)

    def loadFromReady(self):
        self._pcbTable.setRunning(None)
        HARDWARE.timer.stop()
        if not self.__tipo.isEmpty():
            self._dispatcher.load(self.__tipo.next())


class Kernel:
    def __init__(self):
        self._ioDeviceController = IoDeviceController(HARDWARE.ioDevice)
        self._loader = Loader()
        self._pcbTable = PCBTable()
        self._dispatcher = Dispatcher(self._pcbTable)
        self._scheduler = Scheduler(self._pcbTable, self._dispatcher,
                                    # FCFS()
                                    # PriorityNoExp(self._pcbTable)
                                    # PriorityExp(self._pcbTable, self._dispatcher, PriorityNoExp(self._pcbTable))
                                      RoundRobin(FCFS(), 2)
                                    )

        # setup interruption handlers
        HARDWARE.interruptVector.register(NEW_INTERRUPTION_TYPE,
                                          NewInterruptionHandler(self._scheduler, self._pcbTable, self._loader))

        HARDWARE.interruptVector.register(KILL_INTERRUPTION_TYPE,
                                          KillInterruptionHandler(self._scheduler, self._pcbTable, self._dispatcher))

        HARDWARE.interruptVector.register(IO_IN_INTERRUPTION_TYPE,
                                          IoInInterruptionHandler(self._scheduler, self._pcbTable,
                                                                  self._ioDeviceController,
                                                                  self._dispatcher))

        HARDWARE.interruptVector.register(IO_OUT_INTERRUPTION_TYPE,
                                          IoOutInterruptionHandler(self._scheduler, self._ioDeviceController))

        HARDWARE.interruptVector.register(TIME_OUT_INTERRUPTION_TYPE,
                                          TimeOutInterruptionHandler(self._scheduler, self._dispatcher))

        # TODO Nueva interrupcion de hard: TIMEOUT

    @property
    def ioDeviceController(self):
        return self._ioDeviceController

    def __repr__(self):
        return "Kernel :P"
