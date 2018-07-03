from threading import Thread
from time import sleep

from src.hardware.disk import Disk, Swap
from src.hardware.interrupt_vector import InterruptVector
from src.hardware.memory import Memory
from src.structures.asm import ASM
from src.structures.interruptions import Interruption
from src.structures.irq import IRQ
from src.utils.log import logger


class Clock:
    def __init__(self, name, delay, subscribers):
        self._name = name
        self._delay = delay
        self._subscribers = subscribers
        self._running = False
        self._tick_nbr = 0

    def add_subscriber(self, subscriber):
        self._subscribers.insert(0, subscriber)

    def remove_subscriber(self, subscriber):
        self._subscribers.remove(subscriber)

    def stop(self):
        logger.info("Clock", "---- :::: STOP CLOCK {name} ::: -----".format(name=self._name))
        self._running = False

    def _run(self):
        self._running = True
        logger.info("Clock", "---- :::: START CLOCK {name} ::: -----".format(name=self._name))
        while self._running:
            self.tick()

    def start(self):
        if not self._running:
            Thread(target=self._run).start()

    def tick(self):
        logger.info("Clock", "        --------------- {name} tick: {tickNbr} ---------------"
                    .format(name=self._name, tickNbr=self._tick_nbr))
        [subscriber.tick(self._tick_nbr) for subscriber in self._subscribers]
        self._tick_nbr += 1
        sleep(self._delay)

    def do_ticks(self, times):
        logger.info("Clock", "---- :::: CLOCK {name} do_ticks: {times} ::: -----".format(name=self._name, times=times))
        [self.tick() for _ in range(times)]

    def get_info(self):
        return '{name}: tick {nro}'.format(name=self._name, nro=self._tick_nbr)


class Cpu:
    def __init__(self, mmu, interrupt_vector):
        self._mmu = mmu
        self._interrupt_vector = interrupt_vector
        self._pc = -1
        self._ir = None

    def tick(self, _):
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
        return 'CPU({info})'.format(info=self.get_info())

    def get_info(self):
        return 'PC={pc}, IR={ir}'.format(pc=self._pc, ir=self._ir)


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

    def tick(self, _):
        if not self._busy:
            return
        self._ticks_count += 1
        if self._ticks_count > self._time:
            self._busy = False
            self._interrupt_vector.handle(IRQ(Interruption.IO_OUT, self._device))
        else:
            logger.info(self._device, "device {d} - Busy: {tck} of {time}"
                        .format(d=self._device, tck=self._ticks_count, time=self._time))


class Timer:
    def __init__(self, interrupt_vector):
        self._running = False
        self._quantum = -1
        self._tickCount = -1
        self._interrupt_vector = interrupt_vector

    def tick(self, _):
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
        self._frame_size = frame_size
        self._memory = Memory(memory_size)
        self._interrupt_vector = InterruptVector()
        self._disk = Disk(frame_size)
        self._swap = Swap(memory_size, frame_size)
        self._mmu = mmu_type.new_mmu(self._memory, frame_size, self._interrupt_vector)
        self._cpu = Cpu(self._mmu, self._interrupt_vector)
        self._timer = Timer(self._interrupt_vector)

        self._clock_cpu = Clock('CPU', delay, [self._mmu, self._timer, self._cpu])
        keyboard = IODevice(self._interrupt_vector, "KEYBOARD", 1)
        screen = IODevice(self._interrupt_vector, "SCREEN", 2)
        printer = IODevice(self._interrupt_vector, "PRINTER", 3)
        self._io_devices = [keyboard, screen, printer]
        self._clocks = [self._clock_cpu,
                        Clock('KEYBOARD', delay * 1.2, [keyboard]),
                        Clock('SCREEN', delay * 1.5, [screen]),
                        Clock('PRINTER', delay * 2, [printer])]

    def info(self):
        return [['Memory Size', len(self._memory)],
                ['Frame Size', self._frame_size],
                ['Disk usage', self._disk.get_info()],
                ]

    def clock_cpu(self):
        return self._clock_cpu

    def clock_info(self):
        return '\t'.join([c.get_info() for c in self._clocks])

    def tick(self):
        [c.do_ticks(1) for c in self._clocks]

    def switch_on(self):
        logger.info("Hardware", self)
        logger.info("Hardware", " ---- SWITCH ON ---- ")
        [c.start() for c in self._clocks]

    def switch_off(self):
        [c.stop() for c in self._clocks]
        logger.info("Hardware", " ---- SWITCH OFF ---- ")

    def cpu(self):
        return self._cpu

    def interrupt_vector(self):
        return self._interrupt_vector

    def timer(self):
        return self._timer

    def memory(self):
        return self._memory

    def mmu(self):
        return self._mmu

    def io_devices(self):
        return self._io_devices

    def disk(self):
        return self._disk

    def swap(self):
        return self._swap

    def __repr__(self):
        return "HARDWARE state {cpu}\n{mem}".format(cpu=self._cpu, mem=self._memory)
