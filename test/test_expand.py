from unittest import TestCase
from src.utils import expand


class TestExpand(TestCase):
    def test_expand_empty_list(self):
        with self.assertRaises(Exception):
            expand([])

    def test_expand_one_item(self):
         self.assertEqual([1, 'EXIT'], expand([[1]]))

    def test_expand_two_items(self):
         self.assertEqual([1, 1, 'EXIT'], expand([[1, 1]]))

    def test_expand_two_items_in_two_list(self):
         self.assertEqual([1, 1, 2, 2, 'EXIT'], expand([[1, 1], [2 ,2]]))

    def test_expand_one_items_with_exit(self):
         self.assertEqual([1, 'EXIT'], expand([[1], ['EXIT']]))