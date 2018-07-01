from threading import Thread

from prompt_toolkit.shortcuts import clear
from tabulate import tabulate
from termcolor import colored

from src.configuration.algorithm import AlgorithmType
from src.configuration.mmu import MMUType
from src.configuration.mmu_factory import PagedOnDemandFactory
from src.configuration.scheduler import SchedulerType
from src.console import Console
from src.hardware.hardware import Hardware
from src.kernel import Kernel
from src.log import logger
from src.system.file_system import FileSystem
from src.system.memory_manager.algorithms import FCFS
from src.utils import input_default


def _run_system(memory_size, frame_size, scheduler, quantum, mmu_type, algorithm):
    logger.enabled()
    count_frames = memory_size // frame_size
    hardware = Hardware(memory_size, 1, mmu_type, frame_size)
    kernel = Kernel(hardware, scheduler, mmu_type, frame_size, count_frames, quantum, algorithm)
    # logger.show()
    logger.indice()
    print('\n', colored('System Info:', 'cyan'), '\n', tabulate(hardware.info() + kernel.info()))
    input('\nEnter to start...')
    clear()
    t_system = Thread(target=hardware.switch_on)
    t_system.start()
    Console(hardware, kernel, FileSystem(hardware.disk().get_root())).start_console()
    hardware.switch_off()
    t_system.join()
    logger.terminate()


def run_simulator():
    memory_size = input_default('Tamaño de memoria?', '16')
    frame_size = input_default('Tamaño de frame?', '4')
    quantum = None
    scheduler = SchedulerType.choose()
    if SchedulerType.is_rr(scheduler):
        quantum = input_default('RoundRobin Quantum?', '2')
    algorithm = None
    mmu_type = MMUType.choose()
    if mmu_type.is_on_demand():
        algorithm = AlgorithmType.choose()
    _run_system(memory_size, frame_size, scheduler, quantum, mmu_type, algorithm)


def run_priority():
    _run_system(16, 4, 2, None, PagedOnDemandFactory, FCFS())
