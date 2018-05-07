#!/usr/bin/env python

# return A+1 if A > B else A-1
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


class Loader:
    def __init__(self, disk, memory):
        self._next_dir = 0
        self._disk = disk
        self._memory = memory

    def _update_pcb(self, pcb, size):
        pcb['baseDir'] = self._next_dir
        pcb['limit'] = size

    def _load_instructions_size(self, pcb, instructions, size):
        self._update_pcb(pcb, size)
        [self._memory.put(self._next_dir + i, instructions[i]) for i in range(0, size)]
        self._next_dir += size

    def _load_instructions(self, pcb, instructions):
        self._load_instructions_size(pcb, instructions, len(instructions))

    def load(self, pcb):
        self._load_instructions(pcb, self._disk.get(pcb['name']))


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
