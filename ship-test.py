import unittest
from ship import *


class MyTestCase(unittest.TestCase):

    def test_create(self):
        ship = Ship()
        ship.set_pic(1)


if __name__ == '__main__':
    unittest.main()
