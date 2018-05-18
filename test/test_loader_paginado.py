from unittest import TestCase
from unittest.mock import Mock, NonCallableMock, call
from src.so import LoaderPaginado


class TestLoaderPaginado(TestCase):
    def setUp(self):
        self._memory = NonCallableMock()
        self._mm = NonCallableMock(get_frames=Mock(return_value=[0, 5, 2]))
        self._loader_pag = LoaderPaginado(self._memory, self._mm, 2)

    def test_load_page_in_frame_2inst_page0_frame0(self):
        self._loader_pag._load_page_in_frame([1, 2], 0, 0)
        self._memory.put.assert_has_calls([call(0, 1), call(1, 2)])

    def test_load_page_in_frame_3inst_page0_frame0(self):
        self._loader_pag._load_page_in_frame([1, 2, 3], 0, 0)
        self._memory.put.assert_has_calls([call(0, 1), call(1, 2)])

    def test_load_page_in_frame_3inst_page1_frame3(self):
        self._loader_pag._load_page_in_frame([1, 2, 3], 1, 3)
        self._memory.put.assert_has_calls([call(6, 3)])

    def test_load_page_in_frame_4inst_page1_frame1(self):
        self._loader_pag._load_page_in_frame([1, 2, 3, 4], 1, 1)
        self._memory.put.assert_has_calls([call(2, 3), call(3, 4)])

    def test_load_page_in_frame_4inst_page1_frame2(self):
        self._loader_pag._load_page_in_frame([1, 2, 3, 4], 1, 2)
        self._memory.put.assert_has_calls([call(4, 3), call(5, 4)])

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
