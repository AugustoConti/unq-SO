from unittest import TestCase
from unittest.mock import Mock, NonCallableMock, call
from src.system.loader import LoaderPaged


class TestLoaderPaged(TestCase):
    def setUp(self):
        self._disk = NonCallableMock(get_nro_pages=Mock(side_effect=lambda s, f: s//f+(1 if s%f else 0)),
                                     get_page=Mock(side_effect=lambda n, p, f: range(n)[p*f:(p+1)*f]))
        self._memory = NonCallableMock()
        self._mm = NonCallableMock(get_frames=Mock(return_value=[0, 5, 2]))
        self._loader_pag = LoaderPaged(self._disk, self._memory, self._mm, 2)

    def test_load_5_instructions(self):
        self._loader_pag.load({'pid': 1, 'name': 5})
        self._memory.put.assert_has_calls([call(0, 0), call(1, 1),
                                           call(10, 2), call(11, 3),
                                           call(4, 4)])
        self._mm.add_page_table.assert_called_once_with(1, {0: 0, 1: 5, 2: 2})

    def test_load_4_instructions(self):
        self._loader_pag.load({'pid': 1, 'name': 4})
        self._memory.put.assert_has_calls([call(0, 0), call(1, 1),
                                           call(10, 2), call(11, 3)])
        self._mm.add_page_table.assert_called_once_with(1, {0: 0, 1: 5})

    def test_load_3_instructions(self):
        self._loader_pag.load({'pid': 1, 'name': 3})
        self._memory.put.assert_has_calls([call(0, 0), call(1, 1), call(10, 2)])
        self._mm.add_page_table.assert_called_once_with(1, {0: 0, 1: 5})

    def test_load_2_instructions(self):
        self._loader_pag.load({'pid': 1, 'name': 2})
        self._memory.put.assert_has_calls([call(0, 0), call(1, 1)])
        self._mm.add_page_table.assert_called_once_with(1, {0: 0})

    def test_load_1_instructions(self):
        self._loader_pag.load({'pid': 1, 'name': 1})
        self._memory.put.assert_has_calls([call(0, 0)])
        self._mm.add_page_table.assert_called_once_with(1, {0: 0})
