from collections import defaultdict

from tabulate import tabulate

from src.structures.states import State


class Timeline:
    def __init__(self, pcb_table):
        self._pcb_table = pcb_table
        self._ready = defaultdict(int)
        self._retorno = defaultdict(int)
        self._states = defaultdict(list)

    def tick(self, nro):
        if nro == 0:
            return
        for pcb in self._pcb_table:
            if not ('PCB ' + str(pcb.pid)) in self._states[-1]:
                self._states[-1].append('PCB ' + str(pcb.pid))
                [self._states[i].append('-') for i in range(nro - 1)]
            self._states[nro - 1].append(State.mapear(pcb.state))
            self._retorno[pcb.pid] += 1 if pcb.state != State.TERMINATED else 0
            self._ready[pcb.pid] += 1 if pcb.state == State.READY else 0

    def calc(self):
        if 'Return' in self._states:
            del self._states['Return']
        if 'Wait' in self._states:
            del self._states['Wait']
        self._states['Return'] = self._retorno.values()
        self._states['Wait'] = self._ready.values()
        total_retorno = sum(self._retorno.values())
        total_espera = sum(self._ready.values())
        return (tabulate(self._states, headers="keys", tablefmt="fancy_grid"),
                [round(total_retorno / len(self._pcb_table), 2), round(total_espera / len(self._pcb_table), 2)])
