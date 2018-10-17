# coding: utf-8
import unittest
from threadserver import fab


class ToolTest(unittest.TestCase):

    def test_fab(self):
        print (list(fab(10)))


if __name__ == '__main__':
    unittest.main()