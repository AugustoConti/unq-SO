from src.hardware.hardware import Hardware
from src.hardware.mmu import MMUType
from src.kernel import Kernel
from src.log import logger
from src.system.schedulers import SchedulerType
from src.utils import load_programs


def run_simulator():
    logger.enabled()
    memory_size = int(input('Tamaño de memoria? [16] ') or '16')
    frame_size = int(input('Tamaño de frame? [4] ') or '4')
    count_frames = memory_size // frame_size
    sch = SchedulerType.choose()
    quantum = 2
    if SchedulerType.isRR(sch):
        quantum = int(input('RoundRobin Quantum? [2]') or '2')
    mmu = MMUType.choose()
    hardware = Hardware(memory_size, 1, mmu, frame_size)
    load_programs(hardware.disk())
    Kernel(hardware, sch, mmu, frame_size, count_frames, quantum)
    logger.indice()
    logger.show()
    input('Iniciar sistema...')
    hardware.switch_on()
