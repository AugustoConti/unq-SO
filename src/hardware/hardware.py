from time import sleep

from src.hardware.disk import Disk, Swap
from src.hardware.memory import Memory
from src.log import logger
from src.structures.asm import ASM
from src.structures.interruptions import Interruption
from src.structures.irq import IRQ


class InterruptVector:
    def __init__(self):
        self._handlers = dict()

    def register(self, tipo, handler):
        self._handlers[tipo] = handler

    def handle(self, irq):
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
        logger.info("Clock", "---- :::: START CLOCK  ::: -----")
        self._running = True
        tick_nbr = 0
        while self._running:
            self.tick(tick_nbr)
            tick_nbr += 1

    def tick(self, tick_nbr):
        logger.info("Clock", "        --------------- tick: {tickNbr} ---------------".format(tickNbr=tick_nbr))
        [subscriber.tick(tick_nbr) for subscriber in self._subscribers]
        sleep(self._delay)

    def do_ticks(self, times):
        logger.info("Clock", "---- :::: CLOCK do_ticks: {times} ::: -----".format(times=times))
        [self.tick(tickNbr) for tickNbr in range(times)]


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
            logger.info("CPU", "cpu - NOOP")

    def _fetch(self):
        self._ir = self._mmu.fetch(self._pc)
        self._pc += 1

    def _decode(self):
        # decode no hace nada en este caso
        pass

    def _execute(self):
        if ASM.is_exit(self._ir):
            self._interrupt_vector.handle(IRQ(Interruption.KILL))
        elif ASM.is_io(self._ir):
            self._interrupt_vector.handle(IRQ(Interruption.IO_IN, self._ir))
        else:
            logger.info("CPU", "Exec: {instr} in PC={pc}".format(instr=self._ir, pc=self._pc))

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
            self._interrupt_vector.handle(IRQ(Interruption.IO_OUT, self._device))
        else:
            logger.info(self._device, "device {deviceId} - Busy: {ticksCount} of {deviceTime}"
                        .format(deviceId=self._device, ticksCount=self._ticks_count, deviceTime=self._time))


class Timer:
    def __init__(self, interrupt_vector):
        self._running = False
        self._quantum = -1
        self._tickCount = -1
        self._interrupt_vector = interrupt_vector

    def tick(self, tick_nbr):
        if not self._running or self._tickCount < 0:
            return
        logger.info("Timer", "tick: {Count} of {Quantum}".format(Count=self._tickCount, Quantum=self._quantum))
        if self._tickCount == 0:
            self._interrupt_vector.handle(IRQ(Interruption.TIME_OUT))
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


class Hardware:
    def __init__(self, memory_size, delay, mmu_type, frame_size):
        self._memory_size = memory_size
        self._frame_size = frame_size
        self._memory = Memory(memory_size)
        self._interrupt_vector = InterruptVector()
        self._clock = Clock(delay)
        self._io_device = IODevice(self._interrupt_vector, "Printer", 3)
        self._disk = Disk(frame_size)
        self._swap = Swap(memory_size, frame_size)
        self._mmu = mmu_type.new_mmu(self._memory, frame_size, self._interrupt_vector)
        self._cpu = Cpu(self._mmu, self._interrupt_vector)
        self._timer = Timer(self._interrupt_vector)
        self._clock.add_subscribers([self._mmu, self._io_device, self._timer, self._cpu])

    def info(self):
        return [['Memory Size', self._memory_size],
                ['Frame Size', self._frame_size]]

    def switch_on(self):
        logger.info("Hardware", self)
        logger.info("Hardware", " ---- SWITCH ON ---- ")
        self._clock.start()

    def switch_off(self):
        self._clock.stop()
        logger.info("Hardware", "SWITCHING OFF in:")
        for i in [3, 2, 1]:
            logger.info("Hardware", i)
            sleep(1)
        logger.info("Hardware", " ---- SWITCH OFF ---- ")
        sleep(0.5)

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

    def swap(self):
        return self._swap

    def __repr__(self):
        return "HARDWARE state {cpu}\n{mem}".format(cpu=self._cpu, mem=self._memory)
