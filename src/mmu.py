#!/usr/bin/env python


class MMUPaged:
    def __init__(self, memory, frame_size):
        self._page_table = None  # dict(page:frame)
        self._memory = memory
        self._frame_size = frame_size

    def set_page_table(self, table):
        self._page_table = table

    def _get_inst(self, frame, offset):
        return self._memory.get(frame * self._frame_size + offset)

    def fetch(self, log_addr):
        return self._get_inst(self._page_table[log_addr // self._frame_size], log_addr % self._frame_size)


class MMUBasic:
    def __init__(self, memory):
        self._memory = memory
        self._base_dir = 0

    def set_base_dir(self, base_dir):
        self._base_dir = base_dir

    def fetch(self, log_addr):
        return self._memory.get(log_addr + self._base_dir)


class MMU:
    def __init__(self, base):
        self._base = base
        self._base_dir = 0
        self._limit = 999

    def set_base_dir(self, base_dir):
        self._base.set_base_dir(base_dir)

    def set_limit(self, limit):
        self._limit = limit

    def set_page_table(self, table):
        self._base.set_page_table(table)

    def fetch(self, log_addr):
        if log_addr < 0:
            raise IndexError("Invalid Address, {log_addr} is smaller than 0".format(log_addr=log_addr))
        if log_addr >= self._limit:
            raise Exception("Invalid Address, {log_addr} is eq or higher than limit {limit}"
                            .format(limit=self._limit, log_addr=log_addr))
        return self._base.fetch(log_addr)
