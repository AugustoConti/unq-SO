#!/usr/bin/env python

from tabulate import tabulate
from time import sleep
from src.log import logger

INSTRUCTION_IO = 'IO'
INSTRUCTION_CPU = 'CPU'
INSTRUCTION_EXIT = 'EXIT'


# TODO una clase por instruccion, execute
class ASM:
    @classmethod
    def exit(cls):
        return [INSTRUCTION_EXIT]

    @classmethod
    def io(cls):
        return [INSTRUCTION_IO]

    @classmethod
    def cpu(cls, times):
        return [INSTRUCTION_CPU] * times

    @classmethod
    def is_exit(cls, instruction):
        return INSTRUCTION_EXIT == instruction

    @classmethod
    def is_io(cls, instruction):
        return INSTRUCTION_IO == instruction


NEW_INTERRUPTION_TYPE = "#NEW"
KILL_INTERRUPTION_TYPE = "#KILL"
IO_IN_INTERRUPTION_TYPE = "#IO_IN"
IO_OUT_INTERRUPTION_TYPE = "#IO_OUT"
TIME_OUT_INTERRUPTION_TYPE = "#TIME_OUT"


class IRQ:
    def __init__(self, tipo, parameters=None):
        self._tipo = tipo
        self._parameters = parameters

    def parameters(self):
        return self._parameters

    def type(self):
        return self._tipo


class InterruptVector:
    def __init__(self):
        self._handlers = dict()

    def register(self, tipo, handler):
        self._handlers[tipo] = handler

    def handle(self, irq):
        logger.info("Handling {type} irq with parameters = {parameters}"
                    .format(type=irq.type(), parameters=irq.parameters()))
        self._handlers[irq.type()].execute(irq)


class Clock:
    def __init__(self, delay):
        self._subscribers = []
        self._running = False
        self._delay = delay

    def add_subscriber(self, subscriber):
        self._subscribers.append(subscriber)

    def add_subscribers(self, subscribers):
        self._subscribers.extend(subscribers)

    def stop(self):
        self._running = False

    def start(self):
        logger.info("---- :::: START CLOCK  ::: -----")
        self._running = True
        tick_nbr = 0
        while self._running:
            self.tick(tick_nbr)
            tick_nbr += 1

    def tick(self, tick_nbr):
        logger.info("        --------------- tick: {tickNbr} ---------------".format(tickNbr=tick_nbr))
        [subscriber.tick(tick_nbr) for subscriber in self._subscribers]
        sleep(self._delay)

    def do_ticks(self, times):
        logger.info("---- :::: CLOCK do_ticks: {times} ::: -----".format(times=times))
        [self.tick(tickNbr) for tickNbr in range(times)]


class Memory:
    def __init__(self, size):
        self._cells = [''] * size

    def put(self, addr, value):
        self._cells[addr] = value

    def get(self, addr):
        return self._cells[addr]

    def __repr__(self):
        return tabulate(enumerate(self._cells), tablefmt='psql')


class MMU:
    def __init__(self, memory):
        self._memory = memory
        self._base_dir = 0
        self._limit = 999

    def limits(self, base_dir, limit):
        self._base_dir = base_dir
        self._limit = limit

    def fetch(self, logical_address):
        if logical_address < 0:
            raise IndexError("Invalid Address, {logical} is smaller than 0".format(logical=logical_address))
        if logical_address >= self._limit:
            raise Exception("Invalid Address, {logical} is eq or higher than process limit: {limit}"
                            .format(limit=self._limit, logical=logical_address))
        return self._memory.get(logical_address + self._base_dir)


class Cpu:
    def __init__(self, mmu, interrupt_vector):
        self._mmu = mmu
        self._interrupt_vector = interrupt_vector
        self._pc = -1
        self._ir = None

    def tick(self, tick_nbr):
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
        if ASM.is_exit(self._ir):
            self._interrupt_vector.handle(IRQ(KILL_INTERRUPTION_TYPE))
        elif ASM.is_io(self._ir):
            self._interrupt_vector.handle(IRQ(IO_IN_INTERRUPTION_TYPE, self._ir))
        else:
            logger.info("cpu - Exec: {instr}, PC={pc}".format(instr=self._ir, pc=self._pc))

    def get_pc(self):
        return self._pc

    def set_pc(self, addr):
        self._pc = addr

    def __repr__(self):
        return "CPU(PC={pc})".format(pc=self._pc)


class IODevice:
    def __init__(self, interrupt_vector, device, time):
        self._interrupt_vector = interrupt_vector
        self._device = device
        self._time = time
        self._busy = False
        self._ticks_count = 0
        self._operation = None

    def device_id(self):
        return self._device

    def is_idle(self):
        return not self._busy

    def execute(self, operation):
        if self._busy:
            raise Exception("Device {id} is busy, can't  execute operation: {op}"
                            .format(id=self._device, op=operation))
        self._busy = True
        self._ticks_count = 0
        self._operation = operation

    def tick(self, tick_nbr):
        if not self._busy:
            return
        self._ticks_count += 1
        if self._ticks_count > self._time:
            self._busy = False
            self._interrupt_vector.handle(IRQ(IO_OUT_INTERRUPTION_TYPE, self._device))
        else:
            logger.info("device {deviceId} - Busy: {ticksCount} of {deviceTime}"
                        .format(deviceId=self._device, ticksCount=self._ticks_count, deviceTime=self._time))


class Disk:
    def __init__(self):
        self._programs = dict()

    def add(self, name, program):
        self._programs[name] = program
        return self

    def add_all(self, programs):
        [self.add(name, inst) for name, inst in programs.items()]

    def get(self, name):
        return self._programs[name]


class Timer:
    def __init__(self, interrupt_vector):
        self._running = False
        self._quantum = -1
        self._tickCount = -1
        self._interrupt_vector = interrupt_vector

    def tick(self, tick_nbr):
        if not self._running or self._tickCount < 0:
            return
        logger.info("Timer - tick: {Count} of {Quantum}".format(Count=self._tickCount, Quantum=self._quantum))
        if self._tickCount == 0:
            self._interrupt_vector.handle(IRQ(TIME_OUT_INTERRUPTION_TYPE))
        else:
            self._tickCount -= 1

    def reset(self, ajuste=False):
        self._tickCount = self._quantum - (1 if ajuste else 0)

    def stop(self):
        self._tickCount = -1

    def start(self, quantum):
        if quantum < 1:
            raise Exception("Quantum: {q} is smaller than 1".format(q=quantum))
        self._quantum = quantum
        self._running = True
        self.reset()


class Hardware:
    def __init__(self, memory_size, delay):
        self._memory = Memory(memory_size)
        self._interrupt_vector = InterruptVector()
        self._clock = Clock(delay)
        self._io_device = IODevice(self._interrupt_vector, "Printer", 3)
        self._disk = Disk()
        self._mmu = MMU(self._memory)
        self._cpu = Cpu(self._mmu, self._interrupt_vector)
        self._timer = Timer(self._interrupt_vector)
        self._clock.add_subscribers([self._io_device, self._timer, self._cpu])

    def switch_on(self):
        logger.info(self)
        logger.info(" ---- SWITCH ON ---- ")
        self._clock.start()

    def switch_off(self):
        self._clock.stop()
        logger.info(" ---- SWITCH OFF ---- ")

    def cpu(self):
        return self._cpu

    def clock(self):
        return self._clock

    def interrupt_vector(self):
        return self._interrupt_vector

    def timer(self):
        return self._timer

    def memory(self):
        return self._memory

    def mmu(self):
        return self._mmu

    def io_device(self):
        return self._io_device

    def disk(self):
        return self._disk

    def __repr__(self):
        return "HARDWARE state {cpu}\n{mem}".format(cpu=self._cpu, mem=self._memory)
