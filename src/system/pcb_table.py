from src.structures.states import State


class PCBTable:
    def __init__(self, table):
        self._table = table
        self._last_id = 0
        self._pid_running = None

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
            self.set_pcb_state(pid, State.RUNNING)
        return self.get_running()

    def add_pcb(self, pcb):
        self._table[pcb.pid] = pcb

    def set_pcb_state(self, pid, state):
        self._table[pid].state = state

    def get_priority(self, pid):
        return self._table[pid].priority

    def get_intructions_left(self, pid):
        pcb = self._table[pid]
        return pcb.limit - pcb.pc
