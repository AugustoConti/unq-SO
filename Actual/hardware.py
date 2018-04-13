#!/usr/bin/env python

from tabulate import tabulate
from time import sleep
from log import logger

#  Estas son la instrucciones soportadas por nuestro CPU
INSTRUCTION_IO = 'IO'
INSTRUCTION_CPU = 'CPU'
INSTRUCTION_EXIT = 'EXIT'


# Helper for emulated machine code..
class ASM:
    @classmethod
    def EXIT(cls, times):
        return [INSTRUCTION_EXIT] * times

    @classmethod
    def IO(cls):
        return INSTRUCTION_IO

    @classmethod
    def CPU(cls, times):
        return [INSTRUCTION_CPU] * times

    @classmethod
    def isEXIT(cls, instruction):
        return INSTRUCTION_EXIT == instruction

    @classmethod
    def isIO(cls, instruction):
        return INSTRUCTION_IO == instruction


#  Estas son la interrupciones soportadas por nuestro Kernel
NEW_INTERRUPTION_TYPE = "#NEW"
KILL_INTERRUPTION_TYPE = "#KILL"
IO_IN_INTERRUPTION_TYPE = "#IO_IN"
IO_OUT_INTERRUPTION_TYPE = "#IO_OUT"
TIME_OUT_INTERRUPTION_TYPE = "#TIME_OUT"


# emulates an Interrupt request
class IRQ:
    def __init__(self, tipo, parameters=None):
        self._type = tipo
        self._parameters = parameters

    @property
    def parameters(self):
        return self._parameters

    @property
    def type(self):
        return self._type


# emulates the Interrupt Vector Table
class InterruptVector:
    def __init__(self):
        self._handlers = dict()

    def register(self, interruptionType, interruptionHandler):
        self._handlers[interruptionType] = interruptionHandler

    def handle(self, irq):
        logger.info("Handling {type} irq with parameters = {parameters}"
                 .format(type=irq.type, parameters=irq.parameters))
        self._handlers[irq.type].execute(irq)


# emulates the Internal Clock
class Clock:
    def __init__(self):
        self._subscribers = []
        self._running = False

    def addSubscriber(self, subscriber):
        self._subscribers.append(subscriber)

    def stop(self):
        self._running = False

    def start(self):
        logger.info("---- :::: START CLOCK  ::: -----")
        self._running = True
        tickNbr = 0
        while self._running:
            self.tick(tickNbr)
            tickNbr += 1

    def tick(self, tickNbr):
        logger.info("        --------------- tick: {tickNbr} ---------------".format(tickNbr=tickNbr))
        # notify all subscriber that a new clock cycle has started
        for subscriber in self._subscribers:
            subscriber.tick(tickNbr)
        # wait 1 second and keep looping
        sleep(0.1)

    def do_ticks(self, times):
        logger.info("---- :::: CLOCK do_ticks: {times} ::: -----".format(times=times))
        for tickNbr in range(0, times):
            self.tick(tickNbr)


# emulates the main memory (RAM)
class Memory:
    def __init__(self, size):
        self._cells = [''] * size

    def put(self, addr, value):
        self._cells[addr] = value

    def get(self, addr):
        return self._cells[addr]

    def __repr__(self):
        return tabulate(enumerate(self._cells), tablefmt='psql')


# emulates the Memory Management Unit (MMU)
class MMU:
    def __init__(self, memory):
        self._memory = memory
        self._baseDir = 0
        self._limit = 999

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, limit):
        self._limit = limit

    @property
    def baseDir(self):
        return self._baseDir

    @baseDir.setter
    def baseDir(self, baseDir):
        self._baseDir = baseDir

    def fetch(self, logicalAddress):
        if logicalAddress >= self._limit:
            raise Exception("Invalid Address,  {logicalAddress} is eq or higher than process limit: {limit}"
                            .format(limit=self._limit, logicalAddress=logicalAddress))
        return self._memory.get(logicalAddress + self._baseDir)


# emulates the main Central Processor Unit
class Cpu:
    def __init__(self, mmu, interruptVector):
        self._mmu = mmu
        self._interruptVector = interruptVector
        self._pc = -1
        self._ir = None

    def tick(self, tickNbr):
        if self._pc > -1:
            self._fetch()
            self._decode()
            self._execute()
        else:
            logger.info("cpu - NOOP")

    def _fetch(self):
        self._ir = self._mmu.fetch(self._pc)
        self._pc += 1

    def _decode(self):
        # decode no hace nada en este caso
        pass

    def _execute(self):
        if ASM.isEXIT(self._ir):
            self._interruptVector.handle(IRQ(KILL_INTERRUPTION_TYPE))
        elif ASM.isIO(self._ir):
            self._interruptVector.handle(IRQ(IO_IN_INTERRUPTION_TYPE, self._ir))
        else:
            logger.info("cpu - Exec: {instr}, PC={pc}".format(instr=self._ir, pc=self._pc))

    @property
    def pc(self):
        return self._pc

    @pc.setter
    def pc(self, addr):
        self._pc = addr

    def __repr__(self):
        return "CPU(PC={pc})".format(pc=self._pc)


# emulates an Input/output device of the Hardware
class AbstractIODevice:
    def __init__(self, deviceId, deviceTime):
        self._deviceId = deviceId
        self._deviceTime = deviceTime
        self._busy = False
        self._ticksCount = 0
        self._operation = None

    @property
    def deviceId(self):
        return self._deviceId

    @property
    def is_busy(self):
        return self._busy

    @property
    def is_idle(self):
        return not self._busy

    # executes an I/O instruction
    def execute(self, operation):
        if self._busy:
            raise Exception("Device {id} is busy, can't  execute operation: {op}"
                            .format(id=self.deviceId, op=operation))
        self._busy = True
        self._ticksCount = 0
        self._operation = operation

    def tick(self, tickNbr):
        if self._busy:
            self._ticksCount += 1
            if self._ticksCount > self._deviceTime:
                # operation execution has finished
                self._busy = False
                ioOutIRQ = IRQ(IO_OUT_INTERRUPTION_TYPE, self._deviceId)
                HARDWARE.interruptVector.handle(ioOutIRQ)
            else:
                logger.info("device {deviceId} - Busy: {ticksCount} of {deviceTime}"
                         .format(deviceId=self.deviceId,
                                 ticksCount=self._ticksCount,
                                 deviceTime=self._deviceTime))


class PrinterIODevice(AbstractIODevice):
    def __init__(self):
        super(PrinterIODevice, self).__init__("Printer", 3)


class Disc:
    def __init__(self):
        self._programs = dict()

    def add(self, name, program):
        self._programs[name] = program
        return self

    def get(self, name):
        return self._programs[name]

# emulates the Hardware that were the Operative System run
class Hardware:
    def __init__(self):
        self._memory = None
        self._interruptVector = None
        self._clock = None
        self._ioDevice = None
        self._mmu = None
        self._cpu = None
        self._disc = Disc()

    # Setup our hardware
    def setup(self, memorySize):
        # add the components to the "motherboard"
        self._memory = Memory(memorySize)
        self._interruptVector = InterruptVector()
        self._clock = Clock()
        self._ioDevice = PrinterIODevice()
        self._mmu = MMU(self._memory)
        self._cpu = Cpu(self._mmu, self._interruptVector)
        self._clock.addSubscriber(self._ioDevice)
        self._clock.addSubscriber(self._cpu)

    def switchOn(self):
        logger.info(" ---- SWITCH ON ---- ")
        return self.clock.start()

    def switchOff(self):
        self.clock.stop()
        logger.info(" ---- SWITCH OFF ---- ")

    @property
    def cpu(self):
        return self._cpu

    @property
    def clock(self):
        return self._clock

    @property
    def interruptVector(self):
        return self._interruptVector

    @property
    def memory(self):
        return self._memory

    @property
    def mmu(self):
        return self._mmu

    @property
    def ioDevice(self):
        return self._ioDevice

    @property
    def disc(self):
        return self._disc

    def __repr__(self):
        return "HARDWARE state {cpu}\n{mem}".format(cpu=self._cpu, mem=self._memory)


# HARDWARE is a global variable, can be access from any
HARDWARE = Hardware()
