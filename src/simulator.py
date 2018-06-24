from threading import Thread

from tabulate import tabulate
from termcolor import colored

from src.console import start_console
from src.hardware.hardware import Hardware
from src.hardware.mmu import MMUType
from src.kernel import Kernel
from src.log import logger
from src.system.schedulers import SchedulerType
from src.utils import load_programs, input_default


def run_simulator():
    logger.enabled()
    memory_size = input_default('Tamaño de memoria?', '16')
    frame_size = input_default('Tamaño de frame?', '4')
    count_frames = memory_size // frame_size
    sch = SchedulerType.choose()
    quantum = 2
    if SchedulerType.isRR(sch):
        quantum = input_default('RoundRobin Quantum?', '2')
    mmu = MMUType.choose()
    hardware = Hardware(memory_size, 1, mmu, frame_size)
    load_programs(hardware.disk())
    kernel = Kernel(hardware, sch, mmu, frame_size, count_frames, quantum)
    logger.show()
    logger.indice()
    print('\n', colored('System Info:', 'cyan'), '\n', tabulate(hardware.info() + kernel.info()), '\n')
    input('Enter to start...')
    t_system = Thread(target=hardware.switch_on)
    t_system.start()
    start_console()
    hardware.switch_off()
    t_system.join()
    logger.terminate()
