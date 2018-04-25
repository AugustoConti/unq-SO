#!/usr/bin/env python

# return A+1 if A > B else A-1
from src.initializer import registerHandlers
from src.schedulers import *


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
        logger.info(" IO loading pid: {pid}, instruction: {instruction}".format(pid=pair['pid'], instruction=pair['instruction']))
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
        pcb['state'] = STATE_RUNNING
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
        self._table = dict()
        self._pidRunning = None

    @property
    def pcbList(self):
        return self._table.values()

    def getPID(self):
        self._lastID += 1
        return self._lastID

    def isRunning(self):
        return self._pidRunning is not None

    def getRunning(self):
        return self.getPCB(self._pidRunning) if self.isRunning else None

    def getRunningPid(self):
        return self._pidRunning

    def setRunning(self, pid):
        self._pidRunning = pid

    def addPCB(self, pcb):
        self._table[pcb['pid']] = pcb

    def getPCB(self, pid):
        return self._table[pid]

    def getPriority(self, pid):
        return self.getPCB(pid)['priority']


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

        registerHandlers(self._scheduler, self._pcbTable, self._loader, self._dispatcher, self._ioDeviceController)

    @property
    def ioDeviceController(self):
        return self._ioDeviceController

    def pcbTable(self):
        return self._pcbTable

    def __repr__(self):
        return "Kernel"
