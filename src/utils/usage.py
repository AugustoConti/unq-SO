class Usage:
    def __init__(self, name, used, free):
        self._name = name
        self._used = used
        self._free = free

    def to_dict(self):
        return {'name': self._name,
                'total': str(self._used + self._free) + 'B',
                'used': str(self._used) + 'B',
                'free': str(self._free) + 'B',
                'porc': str(round(self._used * 100 / (self._used + self._free), 2)) + '%',
                }

    def __repr__(self):
        return ', '.join(['{k}: {v}'.format(k=k, v=v) for k, v in self.to_dict().items() if k != 'name'])
