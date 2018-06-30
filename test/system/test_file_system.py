from unittest import TestCase

from src.hardware.disk import Folder, File
from src.system.file_system import *


class TestFileSystem(TestCase):
    def setUp(self):
        cracks = Folder('cracks', [], [])
        games = Folder('games', [cracks], [File('cs'), File('fifa')])
        self._fs = FileSystem(Folder('/', [games], [File('git')]))

    def test_cd_back_root(self):
        self._fs.cd('..')
        self.assertEqual('/', self._fs.path())

    def test_cd_back_on_folder(self):
        self._fs.cd('games')
        self._fs.cd('..')
        self.assertEqual('/', self._fs.path())

    def test_cd_back_on_folder_games(self):
        self._fs.cd('games')
        self._fs.cd('cracks')
        self._fs.cd('..')
        self.assertEqual('/games/', self._fs.path())

    def test_cd_carpeta_existente(self):
        self.assertTrue(self._fs.cd('games'))
        self.assertEqual('/games/', self._fs.path())

    def test_cd_carpeta_inexistente(self):
        self.assertFalse(self._fs.cd('windows'))

    def test_cd_archivo(self):
        self.assertFalse(self._fs.cd('git'))

    def test_ls_root(self):
        self.assertEqual((['games'], ['git']), self._fs.ls())

    def test_ls_on_folder(self):
        self._fs.cd('games')
        self.assertEqual((['cracks'], ['cs', 'fifa']), self._fs.ls())

    def test_ls_on_empty_folder(self):
        self._fs.cd('games')
        self._fs.cd('cracks')
        self.assertEqual(([], []), self._fs.ls())

    def test_exe_folder(self):
        self.assertFalse(self._fs.exe('games'))

    def test_exe_file(self):
        self.assertTrue(self._fs.exe('git'))
