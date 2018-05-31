from unittest import TestCase
from unittest.mock import Mock, NonCallableMock, call
from src.system.loader import LoaderPagedOnDemand


class TestLoaderPagedOnDemand(TestCase):
    def setUp(self):
        self._base = NonCallableMock()
        self._mm = NonCallableMock(get_frames=Mock(return_value=[0, 5, 2]))
        self._loader = LoaderPagedOnDemand(self._base, self._mm)

    def test_load(self):
        self.fail("FALTA IMPLEMENTAR")