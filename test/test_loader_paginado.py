from unittest import TestCase
from unittest.mock import Mock, NonCallableMock, call
from src.so import LoaderPaginado


class TestLoaderPaginado(TestCase):
    def setUp(self):
        self._memory = NonCallableMock()
        self._mm = NonCallableMock(get_frames=Mock(return_value=[0, 5, 2]))
        self._loader_pag = LoaderPaginado(self._memory, self._mm, 2)

    def test_load_5_instructions(self):
        self._loader_pag.load_instructions({'pid': 1}, [1, 2, 3, 4, 5])
        self._memory.put.assert_has_calls([call(0, 1), call(1, 2),
                                           call(10, 3), call(11, 4),
                                           call(4, 5)])
        self._mm.add_page_table.assert_called_once_with(1, {0: 0, 1: 5, 2: 2})

    def test_load_4_instructions(self):
        self._loader_pag.load_instructions({'pid': 1}, [1, 2, 3, 4])
        self._memory.put.assert_has_calls([call(0, 1), call(1, 2),
                                           call(10, 3), call(11, 4)])
        self._mm.add_page_table.assert_called_once_with(1, {0: 0, 1: 5})

    def test_load_3_instructions(self):
        self._loader_pag.load_instructions({'pid': 1}, [1, 2, 3])
        self._memory.put.assert_has_calls([call(0, 1), call(1, 2), call(10, 3)])
        self._mm.add_page_table.assert_called_once_with(1, {0: 0, 1: 5})

    def test_load_2_instructions(self):
        self._loader_pag.load_instructions({'pid': 1}, [2, 3])
        self._memory.put.assert_has_calls([call(0, 2), call(1, 3)])
        self._mm.add_page_table.assert_called_once_with(1, {0: 0})

    def test_load_1_instructions(self):
        self._loader_pag.load_instructions({'pid': 1}, [3])
        self._memory.put.assert_has_calls([call(0, 3)])
        self._mm.add_page_table.assert_called_once_with(1, {0: 0})

    def test_load_0_instructions(self):
        with self.assertRaises(Exception):
            self._loader_pag.load_instructions({'pid': 1}, [])
        self._memory.put.assert_not_called()
