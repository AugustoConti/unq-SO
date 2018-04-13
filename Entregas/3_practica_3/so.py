#!/usr/bin/env python

# return A+1 if A > B else A-1

from hardware import *
from log import logger


class Expand:
    def __init__(self, instructions):
        self._instructions = instructions

    def expand(self):
        expanded = []
        for i in self._instructions:
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
        return self._device.is_busy or len(self._waiting_queue) > 0

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
        if len(self._waiting_queue) > 0 and self._device.is_idle:
            self.__load(self._waiting_queue.pop())

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
        logger.info(" CPU running: {currentPCB}".format(currentPCB=pcb))


class Loader:
    def __init__(self):
        self._nextDir = 0

    def load(self, pcb, program):
        instructions = HARDWARE.disc.get(program)
        progSize = len(instructions)
        pcb['baseDir'] = self._nextDir
        pcb['limit'] = progSize
        for i in range(0, progSize):
            HARDWARE.memory.put(self._nextDir + i, instructions[i])
        self._nextDir += progSize


class PCBTable:
    def __init__(self):
        self._lastID = 0  # Last PID of PCBs
        self._tabla = dict()  # list of all PCB
        self._pidRunning = None  # PCB Running

    def getPID(self):
        self._lastID += 1
        return self._lastID

    def isRunning(self):
        return self._pidRunning is not None

    def getRunning(self):
        return None if self._pidRunning is None else self._tabla[self._pidRunning]

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
    def __init__(self):
        pass

    def execute(self, irq):
        pass


class RoundRobin:
    def __init__(self):
        pass


class FCFS:
    def add(self, ready, pid):
        ready.append(pid)

    def next(self, ready):
        return ready.pop()


class PriorityBase:
    def __init__(self, pcbTable):
        self._pcbTable = pcbTable

    def next(self, ready):
        pidMax = 0
        priorityMax = 10
        for i in ready:
            if self._pcbTable.getPriority(i) < priorityMax:
                pidMax = i
                priorityMax = self._pcbTable.getPriority(i)
        ready.remove(pidMax)
        return pidMax


class PriorityExp:
    def __init__(self, pcbTable, dispatcher, base):
        self._pcbTable = pcbTable
        self._dispatcher = dispatcher
        self._base = base

    def add(self, ready, pid):
        pcbRun = self._pcbTable.getRunning()
        if self._pcbTable.getPriority(pid) < pcbRun['priority']:
            self._dispatcher.save()
            self._dispatcher.load(pid)
            ready.append(pcbRun['pid'])
            logger.info("PCB entrante con mayor prioridad que running!")
        else:
            ready.append(pid)

    def next(self, ready):
        return self._base.next(ready)


class PriorityNoExp:
    def __init__(self, base):
        self._base = base

    def add(self, ready, pid):
        ready.append(pid)

    def next(self, ready):
        return self._base.next(ready)


class Scheduler:
    def __init__(self, pcbTable, dispatcher, tipo):
        self.__tipo = tipo
        self._pcbTable = pcbTable
        self._dispatcher = dispatcher
        self._ready_queue = []

    def runOrAddQueue(self, pid):
        if self._pcbTable.isRunning():
            self.__tipo.add(self._ready_queue, pid)
        else:
            self._dispatcher.load(pid)

    def loadFromReady(self):
        self._pcbTable.setRunning(None)
        if len(self._ready_queue) > 0:
            self._dispatcher.load(self.__tipo.next(self._ready_queue))


class Kernel:
    def __init__(self):
        self._ioDeviceController = IoDeviceController(HARDWARE.ioDevice)
        self._loader = Loader()
        self._pcbTable = PCBTable()
        self._dispatcher = Dispatcher(self._pcbTable)
        self._scheduler = Scheduler(self._pcbTable, self._dispatcher,
                            # FCFS()
                            # PriorityNoExp(PriorityBase(self._pcbTable))
                             PriorityExp(self._pcbTable, self._dispatcher, PriorityBase(self._pcbTable))
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
                                          TimeOutInterruptionHandler())

        # TODO Nueva interrupcion de hard: TIMEOUT

    @property
    def ioDeviceController(self):
        return self._ioDeviceController

    def execute(self, program, priority = 5):
        HARDWARE.interruptVector.handle(IRQ(NEW_INTERRUPTION_TYPE,{'program': program, 'priority': priority}))

    def __repr__(self):
        return "Kernel :P"
