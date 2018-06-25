from threading import Thread

from tabulate import tabulate
from termcolor import colored

from src.console import Consola
from src.hardware.hardware import Hardware
from src.hardware.mmu import MMUType
from src.kernel import Kernel
from src.log import logger
from src.system.memory_manager.algorithms import AlgorithmType, FCFS
from src.system.schedulers import SchedulerType
from src.utils import input_default


def _run_system(memory_size, frame_size, scheduler, quantum, mmu, algorithm):
    logger.enabled()
    count_frames = memory_size // frame_size
    hardware = Hardware(memory_size, 1, mmu, frame_size)
    kernel = Kernel(hardware, scheduler, mmu, frame_size, count_frames, quantum, algorithm)
    logger.show()
    logger.indice()
    print('\n', colored('System Info:', 'cyan'), '\n', tabulate(hardware.info() + kernel.info()))
    input('\nEnter to start...')
    t_system = Thread(target=hardware.switch_on)
    t_system.start()
    Consola(hardware, kernel).start_console()
    hardware.switch_off()
    t_system.join()
    logger.terminate()


def run_simulator():
    memory_size = input_default('Tamaño de memoria?', '16')
    frame_size = input_default('Tamaño de frame?', '4')
    quantum = 2
    scheduler = SchedulerType.choose()
    if SchedulerType.isRR(scheduler):
        quantum = input_default('RoundRobin Quantum?', '2')
    algorithm = 1
    mmu = MMUType.choose()
    if MMUType.isOnDemand(mmu):
        algorithm = AlgorithmType.choose()
    _run_system(memory_size, frame_size, scheduler, quantum, mmu, algorithm)


def run_priority():
    _run_system(16, 4, 2, 2, 2, FCFS())
