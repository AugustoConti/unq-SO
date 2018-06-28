class FileSystem:
    def __init__(self, raiz):
        self._raiz = raiz
        self._actual = raiz

    def path(self):
        return self._actual.path()

    def ls(self):
        return self._actual.ls()

    def cd(self, folder):
        self._actual = self._actual.cd(folder)

    def exe(self, prog):
        return self._actual.exe(prog)


class File:
    def __init__(self, name):
        self.name = name


class Folder:
    def __init__(self, name, folders, files):
        self.name = name
        self._up = self
        self._folders = folders
        self._files = files
        [f.set_up(self) for f in folders]

    def set_up(self, up):
        self._up = up

    def path(self):
        if self._up == self:
            return self.name
        else:
            return self._up.path() + self.name + '/'

    def ls(self):
        return [f.name for f in self._folders], [f.name for f in self._files]

    def cd(self, folder):
        if folder == '..':
            return self._up
        res = [f for f in self._folders if f.name == folder]
        if len(res) < 1:
            raise Exception('cd: {f}: No such directory'.format(f=folder))
        return res[0]

    def exe(self, prog):
        res = [f for f in self._files if f.name == prog]
        if len(res) < 1:
            raise Exception('{c}: command not found'.format(c=prog))
        return prog
