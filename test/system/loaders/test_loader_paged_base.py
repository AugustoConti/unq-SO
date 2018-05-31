from unittest import TestCase
from unittest.mock import Mock, NonCallableMock, call
from src.system.loader import LoaderPagedBase


class TestLoaderPagedBase(TestCase):
    def setUp(self):
        self._disk = NonCallableMock(get_nro_pages=Mock(side_effect=lambda s, f: s//f+(1 if s%f else 0)),
                                     get_page=Mock(side_effect=lambda n, p, f: range(n)[p*f:(p+1)*f]))
        self._memory = NonCallableMock()
        self._mm = NonCallableMock(get_frames=Mock(return_value=[0, 5, 2]))
        self._loader = LoaderPagedBase(self._disk, self._memory, self._mm, 2)

    def test_load(self):
        self.fail("FALTA IMPLEMENTAR")