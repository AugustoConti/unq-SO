from src.utils.log import logger


class ControllerDevices:
    def __init__(self, devices):
        self._devices = devices

    def run_operation(self, pid, instruction):
        self._devices[instruction.split()[1]].run_operation(pid, instruction)

    def get_finished_pid(self, device):
        return self._devices[device].get_finished_pid()


class IoDeviceController:
    def __init__(self, device):
        self._device = device
        self._waiting_queue = []
        self._current_pid = None

    def run_operation(self, pid, instruction):
        pair = {'pid': pid, 'inst': instruction}
        self._waiting_queue.append(pair)
        self.__load_from_waiting()
        logger.info("IoDeviceController", self)

    def get_finished_pid(self):
        finished_pid = self._current_pid
        self._current_pid = None
        self.__load_from_waiting()
        return finished_pid

    def __load(self, pair):
        logger.info("IoDeviceController",
                    " IO loading pid: {pid}, instruction: {inst}".format(pid=pair['pid'], inst=pair['inst']))
        self._current_pid = pair['pid']
        self._device.execute(pair['inst'])

    def __load_from_waiting(self):
        if self._waiting_queue and self._device.is_idle():
            self.__load(self._waiting_queue.pop(0))

    def __repr__(self):
        return "IoDeviceController for {ID} running: {Pid} waiting: {waiting}" \
            .format(ID=self._device.device_id(), Pid=self._current_pid, waiting=self._waiting_queue)
