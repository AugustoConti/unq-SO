#!/usr/bin/env python

# return A+1 if A > B else A-1

from hardware import *
from log import logger


class Program:
    def __init__(self, name, instructions):
        self._name = name
        self._instructions = self.__expand(instructions)

    @property
    def name(self):
        return self._name

    @property
    def instructions(self):
        return self._instructions

    def addinstr(self, instruction):
        self._instructions.append(instruction)

    def __expand(self, instructions):
        expanded = []
        for i in instructions:
            if isinstance(i, list):
                expanded.extend(i)
            else:
                expanded.append(i)

        if not ASM.isEXIT(expanded[-1]):
            expanded.append(INSTRUCTION_EXIT)

        return expanded

    def __repr__(self):
        return "Program({name}, {instructions})".format(name=self._name, instructions=self._instructions)


class IoDeviceController:
    def __init__(self, device):
        self._device = device
        self._waiting_queue = []
        self._currentPCB = None

    @property
    def isBusy(self):
        return self._device.is_busy or len(self._waiting_queue) > 0

    def runOperation(self, pcb, instruction):
        # TODO cambiar pcb por pid?? CONSULTAR
        pair = {'pcb': pcb, 'instruction': instruction}
        self._waiting_queue.append(pair)
        self.__load_from_waiting_queue_if_apply()
        logger.info(self)

    def getFinishedPCB(self):
        finishedPCB = self._currentPCB
        self._currentPCB = None
        self.__load_from_waiting_queue_if_apply()
        return finishedPCB

    def __load(self, pair):
        print(pair)
        self._currentPCB = pair['pcb']
        self._device.execute(pair['instruction'])

    def __load_from_waiting_queue_if_apply(self):
        if len(self._waiting_queue) > 0 and self._device.is_idle:
            self.__load(self._waiting_queue.pop())

    def __repr__(self):
        return "IoDeviceController for {deviceID} running: {currentPCB} waiting: {waiting_queue}" \
            .format(deviceID=self._device.deviceId, currentPCB=self._currentPCB, waiting_queue=self._waiting_queue)


class Dispatcher:
    @classmethod
    def save(cls, pcb):
        pcb['pc'] = HARDWARE.cpu.pc
        HARDWARE.cpu.pc = -1

    @classmethod
    def load(cls, pcb):
        HARDWARE.mmu.baseDir = pcb['baseDir']
        HARDWARE.mmu.limit = pcb['limit']
        HARDWARE.cpu.pc = pcb['pc']
        logger.info(" CPU running: {currentPCB}".format(currentPCB=pcb))


class Loader:
    def __init__(self):
        # next empty address
        self._nextDir = 0

    def load(self, pcb, program):
        instructions = HARDWARE.disc.get(program)
        progSize = len(instructions)
        pcb['baseDir'] = self._nextDir
        pcb['limit'] = progSize
        for i in range(0, progSize):
            HARDWARE.memory.put(self._nextDir + i, instructions[i])
        self._nextDir += progSize


class KillInterruptionHandler:
    def __init__(self, kernel):
        self._kernel = kernel

    def execute(self, irq):
        logger.info(" Finished: {currentPCB}"
                    .format(currentPCB=self._kernel._pcbTable.getRunning()))

        Dispatcher.save(self._kernel._pcbTable.getRunning())
        self._kernel.loadFromReady()


class IoInInterruptionHandler:
    def __init__(self, kernel):
        self._kernel = kernel

    def execute(self, irq):
        Dispatcher.save(self._kernel._pcbTable.getRunning())
        self._kernel.ioDeviceController.runOperation(self._kernel._pcbTable.getRunning(), irq.parameters)
        self._kernel.loadFromReady()


class NewInterruptionHandler:
    def __init__(self, kernel):
        self._kernel = kernel

    def execute(self, irq):
        program = irq.parameters
        pcb = {'pid': self._kernel._pcbTable.getPID(),
               'name': program,
               'pc': 0}
        self._kernel._loader.load(pcb, program)

        self._kernel.addPCB(pcb)
        self._kernel.runOrAddQueue(pcb['pid'])
        logger.info(HARDWARE)


class IoOutInterruptionHandler:
    def __init__(self, kernel):
        self._kernel = kernel

    def execute(self, irq):
        self._kernel.runOrAddQueue(self._kernel.ioDeviceController.getFinishedPCB()['pid'])
        logger.info(self._kernel.ioDeviceController)


class PCBTable:
    def __init__(self):
        # Last PID of PCBs
        self._lastID = 0
        # list of all PCB
        self._tabla = dict()
        # PCB Running
        self._pidRunning = None

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


# emulates the core of an Operative System
class Kernel:
    def __init__(self):
        # setup interruption handlers
        HARDWARE.interruptVector.register(NEW_INTERRUPTION_TYPE, NewInterruptionHandler(self))
        HARDWARE.interruptVector.register(KILL_INTERRUPTION_TYPE, KillInterruptionHandler(self))
        HARDWARE.interruptVector.register(IO_IN_INTERRUPTION_TYPE, IoInInterruptionHandler(self))
        HARDWARE.interruptVector.register(IO_OUT_INTERRUPTION_TYPE, IoOutInterruptionHandler(self))

        self._ioDeviceController = IoDeviceController(HARDWARE.ioDevice)
        self._loader = Loader()
        self._pcbTable = PCBTable()
        self._ready_queue = []

    @property
    def ioDeviceController(self):
        return self._ioDeviceController

    def execute(self, program):
        HARDWARE.interruptVector.handle(IRQ(NEW_INTERRUPTION_TYPE, program))

    def addPCB(self, pcb):
        self._pcbTable.addPCB(pcb)

    def runOrAddQueue(self, pid):
        if not self._pcbTable.isRunning():
            self._pcbTable.setRunning(pid)
            Dispatcher.load(self._pcbTable.getRunning())
        else:
            self._ready_queue.append(pid)

    def loadFromReady(self):
        self._pcbTable.setRunning(None)
        if len(self._ready_queue) > 0:
            self._pcbTable.setRunning(self._ready_queue.pop())
            Dispatcher.load(self._pcbTable.getRunning())

    def __repr__(self):
        return "Kernel :)"
