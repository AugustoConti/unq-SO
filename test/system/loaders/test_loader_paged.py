from unittest import TestCase
from unittest.mock import Mock, NonCallableMock, call
from src.system.loader import LoaderPagedBase, LoaderPaged, LoaderPagedOnDemand


class TestLoaderPagedBase(TestCase):
    def setUp(self):
        self._tipo = NonCallableMock(load=Mock(side_effect=lambda a, b, c: c))
        self._disk = NonCallableMock(get_nro_pages=Mock(side_effect=lambda s: s),
                                     get_page=Mock(side_effect=lambda n, p: range(p)))
        self._swap = NonCallableMock(swap_out=Mock(side_effect=lambda a: range(a)),
                                     swap_in=Mock(side_effect=lambda p: p))
        self._memory = NonCallableMock(get=Mock(side_effect=lambda d: d))
        self._mm = NonCallableMock(get_frames=Mock(return_value=[0, 5, 2]))

        self._loader = LoaderPagedBase(self._tipo, self._disk, self._swap, self._memory, self._mm, 2)

    def test_load(self):
        self._loader.load({'pid': 1, 'name': 3})
        self._mm.create_page_table.assert_called_once_with(1, [0, 1, 2])

    def test_load_page(self):
        self._loader.load_page('pepe', 2, 5)
        self._memory.put.assert_has_calls([call(10, 0), call(11, 1)])

    def test_swap_out(self):
        self._loader.swap_out(2, 4)
        self._memory.put.assert_has_calls([call(8, 0), call(9, 1)])

    def test_swap_in(self):
        self.assertEquals([4, 5], self._loader.swap_in(2))

class TestLoaderPaged(TestCase):
    def setUp(self):
        self._base = NonCallableMock()
        self._mm = NonCallableMock(get_frame=Mock(return_value=2))
        self._loader = LoaderPaged(self._mm)

    def test_load(self):
        self.assertEquals(2, self._loader.load(self._base, 0, 1))
        self._base.load_page.assert_called_once_with(0, 1, 2)


class TestLoaderPagedOnDemand(TestCase):
    def setUp(self):
        self._loader = LoaderPagedOnDemand()

    def test_load(self):
        self.assertEquals(-1, self._loader.load(0, 0, 0))
