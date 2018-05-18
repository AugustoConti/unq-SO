#!/usr/bin/env python

# return A+1 if A > B else A-1
from builtins import Exception

from src.interruption_handlers import STATE_RUNNING
from src.log import logger


class IoDeviceController:
    def __init__(self, device):
        self._device = device
        self._waiting_queue = []
        self._current_pid = None

    def run_operation(self, pid, instruction):
        pair = {'pid': pid, 'inst': instruction}
        self._waiting_queue.append(pair)
        self.__load_from_waiting()
        logger.info(self)

    def get_finished_pid(self):
        finished_pid = self._current_pid
        self._current_pid = None
        self.__load_from_waiting()
        return finished_pid

    def __load(self, pair):
        logger.info(" IO loading pid: {pid}, instruction: {inst}".format(pid=pair['pid'], inst=pair['inst']))
        self._current_pid = pair['pid']
        self._device.execute(pair['inst'])

    def __load_from_waiting(self):
        if self._waiting_queue and self._device.is_idle():
            self.__load(self._waiting_queue.pop(0))

    def __repr__(self):
        return "IoDeviceController for {ID} running: {Pid} waiting: {waiting}" \
            .format(ID=self._device.device_id(), Pid=self._current_pid, waiting=self._waiting_queue)


class Dispatcher:
    def __init__(self, pcb_table, cpu, mmu, timer):
        self._pcb_table = pcb_table
        self._cpu = cpu
        self._mmu = mmu
        self._timer = timer

    def save(self):
        self._pcb_table.get_running()['pc'] = self._cpu.get_pc()
        self._cpu.set_pc(-1)

    def load(self, pid):
        pcb = self._pcb_table.set_running(pid)
        self._mmu.limits(pcb['baseDir'], pcb['limit'])
        self._cpu.set_pc(pcb['pc'])
        self._timer.reset()
        logger.info(" CPU running: {currentPCB}".format(currentPCB=pcb))


class MemoryManager:
    def __init__(self, count_frames):
        self._free_frames = range(count_frames)
        self._page_table = dict()

    def get_frames(self, count):
        if count > len(self._free_frames):
            raise Exception('Insuficientes frames. Se piden {c} pero hay {q}'
                            .format(c=count, q=len(self._free_frames)))
        ret = self._free_frames[:count]
        self._free_frames = self._free_frames[count:]
        return ret

    def add_page_table(self, pid, table):
        self._page_table[pid] = table


class LoaderComun:
    def __init__(self, memory):
        self._next_dir = 0
        self._memory = memory

    def _update_pcb(self, pcb, size):
        pcb['baseDir'] = self._next_dir
        pcb['limit'] = size

    def load_instructions(self, pcb, instructions):
        size = len(instructions)
        self._update_pcb(pcb, size)
        [self._memory.put(self._next_dir + i, instructions[i]) for i in range(0, size)]
        self._next_dir += size


class LoaderPaginado:
    def __init__(self, memory, mm, frames_size):
        self._memory = memory
        self._mm = mm
        self._frames_size = frames_size

    def _get_value(self, nro_page, idx=0):
        return (nro_page + idx) * self._frames_size

    def _load_page_in_frame(self, instructions, nro_page, frame):
        page = instructions[self._get_value(nro_page):self._get_value(nro_page, 1)]
        [self._memory.put(self._frames_size * frame + i, page[i]) for i in range(len(page))]

    def load_instructions(self, pcb, instructions):
        size = len(instructions)
        page_table = dict()
        pages_count = size // self._frames_size + (1 if size % self._frames_size else 0)
        frames_list = self._mm.get_frames(pages_count)
        for page in range(pages_count):
            self._load_page_in_frame(instructions, page, frames_list[page])
            page_table[page] = frames_list[page]
        self._mm.add_page_table(pcb['pid'], page_table)


class Loader:
    def __init__(self, base, disk):
        self._next_dir = 0
        self._disk = disk
        self._base = base

    def load(self, pcb):
        self._base.load_instructions(pcb, self._disk.get(pcb['name']))


class PCBTable:
    def __init__(self):
        self._last_id = 0
        self._table = dict()
        self._pid_running = None

    def pcb_list(self):
        return self._table.values()

    def get_pid(self):
        self._last_id += 1
        return self._last_id

    def is_running(self):
        return self._pid_running is not None

    def get_running(self):
        return self._table[self._pid_running] if self.is_running() else None

    def get_running_pid(self):
        return self._pid_running

    def set_running(self, pid):
        self._pid_running = pid
        if pid is not None:
            self.set_pcb_state(pid, STATE_RUNNING)
        return self.get_running()

    def add_pcb(self, pcb):
        self._table[pcb['pid']] = pcb

    def set_pcb_state(self, pid, state):
        self._table[pid]['state'] = state

    def get_priority(self, pid):
        return self._table[pid]['priority']
