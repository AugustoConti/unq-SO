#!/usr/bin/env python

from hardware import *
import log



## emulates a compiled program
class Program():

    def __init__(self, name, instructions):
        self._name = name
        self._instructions = self.expand(instructions)

    @property
    def name(self):
        return self._name

    @property
    def instructions(self):
        return self._instructions

    def addInstr(self, instruction):
        self._instructions.append(instruction)

    def expand(self, instructions):
        expanded = []
        for i in instructions:
            if isinstance(i, list):
                ## is a list of instructions
                expanded.extend(i)
            else:
                ## a single instr (a String)
                expanded.append(i)

        ## now test if last instruction is EXIT
        ## if not... add an EXIT as final instruction
        last = expanded[-1]
        if not ASM.isEXIT(last):
            expanded.append(INSTRUCTION_EXIT)

        return expanded

    def __repr__(self):
        return "Program({name}, {instructions})".format(name=self._name, instructions=self._instructions)


## emulates an Input/Output device controller (driver)
class IoDeviceController():

    def __init__(self, device):
        self._device = device
        self._waiting_queue = []
        self._currentPCB = None

    @property
    def isBusy(self):
        return self._device.is_busy or len(self._waiting_queue) > 0

    def runOperation(self, pcb, instruction):
        pair = {'pcb': pcb, 'instruction': instruction}
        # append: adds the element at the end of the queue
        self._waiting_queue.append(pair)
        # try to send the instruction to hardware's device (if is idle)
        self.__load_from_waiting_queue_if_apply()

    def getFinishedPCB(self):
        finishedPCB = self._currentPCB
        self._currentPCB = None
        self.__load_from_waiting_queue_if_apply()
        return finishedPCB

    def __load_from_waiting_queue_if_apply(self):
        if (len(self._waiting_queue) > 0) and self._device.is_idle:
            ## pop(): extracts (deletes and return) the first element in queue
            pair = self._waiting_queue.pop()
            print(pair)
            pcb = pair['pcb']
            instruction = pair['instruction']
            self._currentPCB = pcb
            self._device.execute(instruction)


    def __repr__(self):
        return "IoDeviceController for {deviceID} running: {currentPCB} waiting: {waiting_queue}".format(deviceID=self._device.deviceId, currentPCB=self._currentPCB, waiting_queue=self._waiting_queue)


## emulates the  Interruptions Handlers
class AbstractInterruptionHandler():
    def __init__(self, kernel):
        self._kernel = kernel

    @property
    def kernel(self):
        return self._kernel

    def execute(self, irq):
        log.logger.error("-- EXECUTE MUST BE OVERRIDEN in class {classname}".format(classname=self.__class__.__name__))


class KillInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        self._kernel.handleKill()

class IoInInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        self._kernel.handleIoIn(irq.parameters)


class IoOutInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        self._kernel.handleIoOut()


# emulates the core of an Operative System
class Kernel():

    def __init__(self):
        ## setup interruption handlers
        killHandler = KillInterruptionHandler(self)
        HARDWARE.interruptVector.register(KILL_INTERRUPTION_TYPE, killHandler)

        ioInHandler = IoInInterruptionHandler(self)
        HARDWARE.interruptVector.register(IO_IN_INTERRUPTION_TYPE, ioInHandler)

        ioOutHandler = IoOutInterruptionHandler(self)
        HARDWARE.interruptVector.register(IO_OUT_INTERRUPTION_TYPE, ioOutHandler)

        ## controls the Hardware's I/O Device
        self._ioDeviceController = IoDeviceController(HARDWARE.ioDevice)

        ## Last ID of PCB
        self._id = 0
        ## Next dir of memory empty
        self._nextDir = 0
        ## List of ready process
        self._ready_queue = []
        ## PCB actual corriendo en CPU
        self._currentPCB = None

    def _getID(self):
        self._id += 1
        return self._id

    @property
    def ioDeviceController(self):
        return self._ioDeviceController


    def _load(self, pcb):
        self._currentPCB = pcb
        HARDWARE.mmu.baseDir = pcb['baseDir']
        HARDWARE.mmu.limit = pcb['limit']
        HARDWARE.cpu.pc = pcb['pc']
        log.logger.info(" CPU running: {currentPCB}".format(currentPCB=pcb))

    ## Si no hay nadie corriendo, cargarlo. Sino agregarlo a la cola
    def _loadOrEnqueue(self, pcb):
        if self._currentPCB == None:
            self._load(pcb)
        else:
            self._ready_queue.append(pcb)

    def handleKill(self):
        log.logger.info(" Program {name} Finished: {currentPCB}".format(name=self._currentPCB['name'],currentPCB=self._currentPCB))
        HARDWARE.cpu.pc = -1
        self._currentPCB = None
        if len(self._ready_queue) > 0:
            self._load(self._ready_queue.pop())
        elif not self._ioDeviceController.isBusy:
            HARDWARE.switchOff()

    def handleIoIn(self, operation):
        self._currentPCB['pc'] = HARDWARE.cpu.pc
        HARDWARE.cpu.pc = -1
        self._ioDeviceController.runOperation(self._currentPCB, operation)
        log.logger.info(self._ioDeviceController)
        self._currentPCB = None
        if len(self._ready_queue) > 0:
            self._load(self._ready_queue.pop())

    def handleIoOut(self):
        self._loadOrEnqueue(self._ioDeviceController.getFinishedPCB())
        log.logger.info(self._ioDeviceController)


    def load_program(self, program):
        # loads the program in main memory
        progSize = len(program.instructions)
        for index in range(0, progSize):
            HARDWARE.memory.put(self._nextDir+index, program.instructions[index])
        self._nextDir += progSize

    ## emulates a "system call" for programs execution
    def execute(self, program):
        pcb = {'id': self._getID(),
               'name': program.name,
               'baseDir': self._nextDir,
               'limit': len(program.instructions),
               'pc': 0}
        self.load_program(program)
        log.logger.info(HARDWARE)
        self._loadOrEnqueue(pcb)

    def __repr__(self):
        return "Kernel "
