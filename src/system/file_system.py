# TODO implementar mkdir, touch, rm !!!


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
