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

    def get_page_table(self):
        return self._base.get_page_table()

    def tick(self, tick_nbr):
        self._base.tick(tick_nbr)

    def fetch(self, log_addr):
        if log_addr < 0:
            raise IndexError("Invalid Address, {log_addr} is smaller than 0".format(log_addr=log_addr))
        if log_addr >= self._limit:
            raise Exception("Invalid Address, {log_addr} is eq or higher than limit {limit}"
                            .format(limit=self._limit, log_addr=log_addr))
        return self._base.fetch(log_addr)
