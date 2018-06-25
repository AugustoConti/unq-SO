from src.system.states import State


class PCB:
    def __init__(self, pid=0, name='', base=0, limit=0, priority=0):
        self.pid = pid
        self.name = name
        self.state = State.NEW
        self.pc = 0
        self.baseDir = base
        self.limit = limit
        self.priority = priority

    def to_dict(self):
        return {'pid': self.pid,
                'name': self.name,
                'state': self.state,
                'pc': self.pc,
                'baseDir': self.baseDir,
                'limit': self.limit,
                'priority': self.priority}

    def __repr__(self):
        return "PCB {p} - {n} (State: {s}, pc: {pc}, baseDir: {bd}, limit: {lm}, priority: {pr} )" \
            .format(p=self.pid, n=self.name, s=self.state, pc=self.pc, bd=self.baseDir, lm=self.limit, pr=self.priority)
