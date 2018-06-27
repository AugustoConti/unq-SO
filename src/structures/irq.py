class IRQ:
    def __init__(self, tipo, parameters=None):
        self._tipo = tipo
        self._parameters = parameters

    def parameters(self):
        return self._parameters

    def type(self):
        return self._tipo
