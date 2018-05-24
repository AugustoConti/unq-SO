from builtins import Exception
from src.system.states import State
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


class MemoryManager:
    def __init__(self, count_frames):
        self._free_frames = list(range(count_frames))
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

    def get_page_table(self, pid):
        return self._page_table[pid]

    def kill(self, pid):
        if pid in self._page_table:
            self._free_frames.extend(self._page_table[pid].values())


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
        self._table[pcb['pid']] = pcb

    def set_pcb_state(self, pid, state):
        self._table[pid]['state'] = state

    def get_priority(self, pid):
        return self._table[pid]['priority']
