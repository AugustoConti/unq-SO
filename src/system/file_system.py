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
        if folder == '/':
            self._actual = self._raiz
        elif folder == '..':
            self._actual = self._actual.get_up()
        elif self._actual.has_folder(folder):
            self._actual = self._actual.cd(folder)
        else:
            return False
        return True

    def exe(self, prog):
        return self._actual.exe(prog)
